<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * Main workspace page for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

require_once(__DIR__ . '/../../config.php');

$courseid = required_param('courseid', PARAM_INT);
$course = get_course($courseid);
require_login($course);

$context = \local_ada\access_helper::require_access_in_course((int)$course->id);

$PAGE->set_url(new moodle_url('/local/ada/index.php', ['courseid' => $course->id]));
$PAGE->set_context($context);
$PAGE->set_pagelayout('incourse');
$PAGE->set_title(get_string('workspace_title', 'local_ada'));
$PAGE->set_heading($course->fullname);

$PAGE->requires->js_call_amd('local_ada/assistant', 'init', [$course->id]);

echo $OUTPUT->header();
echo $OUTPUT->render_from_template('local_ada/workspace', [
    'courseid' => $course->id,
    'coursename' => format_string($course->fullname, true, ['context' => $context]),
    'questionbankurl' => (new moodle_url('/question/edit.php', ['courseid' => $course->id]))->out(false),
]);
echo $OUTPUT->footer();

