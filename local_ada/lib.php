<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * Navigation hooks for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

/**
 * Adds the ADA Assistant link to course secondary navigation for authorized teachers.
 *
 * @param navigation_node $navigation
 * @param stdClass $course
 * @param context_course $context
 */
function local_ada_extend_navigation_course(navigation_node $navigation, stdClass $course, context_course $context): void {
    if (!\local_ada\access_helper::can_use_in_course((int)$course->id)) {
        return;
    }

    $url = new moodle_url('/local/ada/index.php', ['courseid' => $course->id]);
    $node = navigation_node::create(
        get_string('pluginname', 'local_ada'),
        $url,
        navigation_node::TYPE_CUSTOM,
        null,
        'local_ada',
        new pix_icon('i/edit', '')
    );
    $navigation->add_node($node);
}

