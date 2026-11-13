<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

namespace local_ada\client;

defined('MOODLE_INTERNAL') || die();

require_once($CFG->libdir . '/filelib.php');

/**
 * HTTP client for communicating with the external ADA Middleware.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class middleware_client {
    /**
     * Calls a JSON POST endpoint on the ADA Middleware.
     *
     * @param string $path Endpoint path (e.g. '/v1/questions/generate').
     * @param array $payload Request payload.
     * @return array Decoded JSON response.
     * @throws \moodle_exception On configuration, network, or HTTP errors.
     */
    public function post_json(string $path, array $payload): array {
        $baseurl = rtrim((string)get_config('local_ada', 'middlewareurl'), '/');
        $token = (string)get_config('local_ada', 'servicetoken');
        $timeout = max(5, (int)get_config('local_ada', 'timeout'));

        if ($baseurl === '' || $token === '') {
            throw new \moodle_exception('error_middleware_unconfigured', 'local_ada');
        }

        $curl = new \curl(['ignoresecurity' => true]);
        $curl->setHeader([
            'Content-Type: application/json',
            'Accept: application/json',
            'X-ADA-Token: ' . $token,
        ]);

        $options = [
            'CURLOPT_TIMEOUT' => $timeout,
            'CURLOPT_CONNECTTIMEOUT' => 5,
        ];

        $raw = $curl->post($baseurl . $path, json_encode($payload, JSON_UNESCAPED_UNICODE), $options);
        $info = $curl->get_info();
        $httpcode = (int)($info['http_code'] ?? 0);

        if ($httpcode < 200 || $httpcode >= 300) {
            $detail = '';
            $decoded = json_decode((string)$raw, true);
            if (is_array($decoded) && !empty($decoded['detail'])) {
                $detail = ' ' . $decoded['detail'];
            } else if ($httpcode === 0 && !empty($curl->error)) {
                $detail = ' ' . $curl->error;
            }
            throw new \moodle_exception('error_middleware_http', 'local_ada', '', $httpcode . $detail);
        }

        $data = json_decode((string)$raw, true);
        if (!is_array($data)) {
            throw new \moodle_exception('error_middleware_http', 'local_ada', '', 'JSON inválido');
        }

        return $data;
    }
}

