<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

namespace local_ada\external;

use core_external\external_api;
use core_external\external_function_parameters;
use core_external\external_single_structure;
use core_external\external_value;
use local_ada\client\middleware_client;

defined('MOODLE_INTERNAL') || die();

/**
 * External API for generating multiple-choice questions via ADA Middleware.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class generate_questions extends external_api {
    /**
     * Parameter definition.
     *
     * @return external_function_parameters
     */
    public static function execute_parameters(): external_function_parameters {
        return new external_function_parameters([
            'courseid' => new external_value(PARAM_INT, 'Course ID'),
            'topic' => new external_value(PARAM_TEXT, 'Topic or base content'),
            'count' => new external_value(PARAM_INT, 'Number of questions (1-10)', VALUE_DEFAULT, 3),
            'difficulty' => new external_value(PARAM_ALPHA, 'Difficulty level', VALUE_DEFAULT, 'intermediate'),
            'provider' => new external_value(PARAM_ALPHA, 'Provider override (auto, groq, gemini)', VALUE_DEFAULT, 'auto'),
            'exportformat' => new external_value(PARAM_ALPHANUMEXT, 'Export format (moodle_xml, gift)', VALUE_DEFAULT, 'moodle_xml'),
        ]);
    }

    /**
     * Executes question generation through the ADA Middleware.
     *
     * @param int $courseid
     * @param string $topic
     * @param int $count
     * @param string $difficulty
     * @param string $provider
     * @param string $exportformat
     * @return array
     */
    public static function execute(
        int $courseid,
        string $topic,
        int $count = 3,
        string $difficulty = 'intermediate',
        string $provider = 'auto',
        string $exportformat = 'moodle_xml'
    ): array {
        global $CFG, $DB;

        $params = self::validate_parameters(self::execute_parameters(), [
            'courseid' => $courseid,
            'topic' => $topic,
            'count' => $count,
            'difficulty' => $difficulty,
            'provider' => $provider,
            'exportformat' => $exportformat,
        ]);

        $context = \context_course::instance($params['courseid']);
        self::validate_context($context);
        require_capability('local/ada:use', $context);

        $course = $DB->get_record('course', ['id' => $params['courseid']], 'id, shortname', MUST_EXIST);
        $moodleversion = str_starts_with((string)$CFG->release, '5.') ? '5.0' : '4.5';

        $client = new middleware_client();
        $result = $client->post_json('/v1/questions/generate', [
            'moodle_version' => $moodleversion,
            'course_shortname' => $course->shortname,
            'topic' => trim($params['topic']),
            'question_type' => 'multichoice',
            'export_format' => $params['exportformat'] === 'gift' ? 'gift' : 'moodle_xml',
            'count' => max(1, min(10, (int)$params['count'])),
            'difficulty' => $params['difficulty'],
            'language' => current_language(),
            'provider' => $params['provider'],
        ]);

        return [
            'providerused' => (string)($result['provider_used'] ?? ''),
            'modelused' => (string)($result['model_used'] ?? ''),
            'latencyms' => (int)($result['latency_ms'] ?? 0),
            'filename' => (string)($result['filename'] ?? 'ada_preguntas.xml'),
            'exportedcontent' => (string)($result['exported_content'] ?? ''),
            'questionsjson' => json_encode($result['questions'] ?? [], JSON_UNESCAPED_UNICODE),
        ];
    }

    /**
     * Return structure definition.
     *
     * @return external_single_structure
     */
    public static function execute_returns(): external_single_structure {
        return new external_single_structure([
            'providerused' => new external_value(PARAM_TEXT, 'LLM provider used'),
            'modelused' => new external_value(PARAM_TEXT, 'Model identifier used'),
            'latencyms' => new external_value(PARAM_INT, 'Inference latency in ms'),
            'filename' => new external_value(PARAM_FILE, 'Suggested XML filename'),
            'exportedcontent' => new external_value(PARAM_RAW, 'Moodle XML content'),
            'questionsjson' => new external_value(PARAM_RAW, 'JSON-encoded questions for preview'),
        ]);
    }
}

