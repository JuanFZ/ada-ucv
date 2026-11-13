<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * English language strings for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

$string['pluginname'] = 'ADA Assistant';
$string['ada:use'] = 'Use ADA teaching assistant';
$string['settings_middlewareurl'] = 'Middleware URL';
$string['settings_middlewareurl_desc'] = 'Base URL of the external ADA Middleware (e.g. http://host.docker.internal:8000).';
$string['settings_servicetoken'] = 'Service token';
$string['settings_servicetoken_desc'] = 'Shared secret token (X-ADA-Token) configured in the Middleware .env file.';
$string['settings_timeout'] = 'Timeout (seconds)';
$string['settings_timeout_desc'] = 'Maximum wait time for Middleware inference responses.';
$string['workspace_title'] = 'ADA — Teaching Assistant';
$string['workspace_subtitle'] = 'Generate multiple-choice questions in Moodle XML format for manual review and import.';
$string['field_topic'] = 'Topic or base content';
$string['field_topic_placeholder'] = 'E.g.: Time complexity (Big-O) and binary search trees...';
$string['field_count'] = 'Number of questions';
$string['field_difficulty'] = 'Difficulty';
$string['difficulty_basic'] = 'Basic';
$string['difficulty_intermediate'] = 'Intermediate';
$string['difficulty_advanced'] = 'Advanced';
$string['field_provider'] = 'AI Provider';
$string['provider_auto'] = 'Automatic (Primary + Fallback)';
$string['btn_generate'] = 'Generate questions';
$string['btn_download_xml'] = 'Download Moodle XML';
$string['generating'] = 'Generating and validating questions...';
$string['preview_title'] = 'Preview before importing';
$string['error_middleware_unconfigured'] = 'ADA Middleware URL or token is not configured in site administration.';
$string['error_middleware_http'] = 'Error communicating with ADA Middleware (HTTP {$a}).';

