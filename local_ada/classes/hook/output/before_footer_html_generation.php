<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

namespace local_ada\hook\output;

defined('MOODLE_INTERNAL') || die();

/**
 * Injects the floating ADA interactive chat drawer in authorized course pages.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class before_footer_html_generation {
    /**
     * Hook callback executed before footer HTML is rendered.
     *
     * @param \core\hook\output\before_footer_html_generation $hook
     */
    public static function callback(\core\hook\output\before_footer_html_generation $hook): void {
        global $OUTPUT, $PAGE;

        if (!isloggedin() || isguestuser()) {
            return;
        }

        if ($PAGE->pagelayout === 'embedded' || $PAGE->pagelayout === 'maintenance') {
            return;
        }

        $coursecontext = $PAGE->context->get_course_context(false);
        if (!$coursecontext || $coursecontext->instanceid == SITEID) {
            return;
        }

        if (!has_capability('local/ada:use', $coursecontext)) {
            return;
        }

        if (strpos($PAGE->url->get_path(), '/local/ada/index.php') !== false) {
            return;
        }

        $courseid = (int)$coursecontext->instanceid;
        $PAGE->requires->js_call_amd('local_ada/chat_drawer', 'init', [$courseid]);

        $html = $OUTPUT->render_from_template('local_ada/chat_drawer', [
            'courseid' => $courseid,
            'fullworkspaceurl' => (new \moodle_url('/local/ada/index.php', ['courseid' => $courseid]))->out(false),
        ]);
        $hook->add_html($html);
    }
}

