<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

namespace local_ada;

defined('MOODLE_INTERNAL') || die();

/**
 * Authorization and category-scope helper for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class access_helper {
    /**
     * Checks whether the current user can use ADA in the given course,
     * respecting both capabilities and allowed course categories.
     *
     * @param int $courseid
     * @return bool
     */
    public static function can_use_in_course(int $courseid): bool {
        if ($courseid <= 0 || $courseid == SITEID) {
            return false;
        }

        $context = \context_course::instance($courseid, IGNORE_MISSING);
        if (!$context || !has_capability('local/ada:use', $context)) {
            return false;
        }

        return self::is_course_in_allowed_categories($courseid);
    }

    /**
     * Enforces access in the given course or throws a permission exception.
     *
     * @param int $courseid
     * @return \context_course
     * @throws \moodle_exception
     */
    public static function require_access_in_course(int $courseid): \context_course {
        $context = \context_course::instance($courseid);
        require_capability('local/ada:use', $context);

        if (!self::is_course_in_allowed_categories($courseid)) {
            throw new \moodle_exception('error_category_restricted', 'local_ada');
        }

        return $context;
    }

    /**
     * Returns true if allowedcategories is empty or the course belongs to
     * an allowed category (including subcategories).
     *
     * @param int $courseid
     * @return bool
     */
    public static function is_course_in_allowed_categories(int $courseid): bool {
        global $DB;

        $raw = trim((string)get_config('local_ada', 'allowedcategories'));
        if ($raw === '') {
            return true;
        }

        $allowed = array_filter(array_map('intval', explode(',', $raw)));
        if (empty($allowed)) {
            return true;
        }

        $course = $DB->get_record('course', ['id' => $courseid], 'id, category');
        if (!$course) {
            return false;
        }

        $cat = $DB->get_record('course_categories', ['id' => $course->category], 'id, path');
        if (!$cat) {
            return false;
        }

        $pathids = array_filter(array_map('intval', explode('/', (string)$cat->path)));
        return !empty(array_intersect($allowed, $pathids));
    }
}

