<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * External service definitions for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

$functions = [
    'local_ada_generate_questions' => [
        'classname' => 'local_ada\external\generate_questions',
        'description' => 'Genera preguntas de opción múltiple en formato Moodle XML mediante el Middleware de ADA.',
        'type' => 'write',
        'ajax' => true,
        'capabilities' => 'local/ada:use',
    ],
];

