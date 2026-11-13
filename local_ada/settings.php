<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * Admin settings for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

if ($hassiteconfig) {
    $settings = new admin_settingpage('local_ada', get_string('pluginname', 'local_ada'));
    $ADMIN->add('localplugins', $settings);

    $settings->add(new admin_setting_configtext(
        'local_ada/middlewareurl',
        get_string('settings_middlewareurl', 'local_ada'),
        get_string('settings_middlewareurl_desc', 'local_ada'),
        'http://host.docker.internal:8000',
        PARAM_URL
    ));

    $settings->add(new admin_setting_configpasswordunmask(
        'local_ada/servicetoken',
        get_string('settings_servicetoken', 'local_ada'),
        get_string('settings_servicetoken_desc', 'local_ada'),
        ''
    ));

    $settings->add(new admin_setting_configtext(
        'local_ada/timeout',
        get_string('settings_timeout', 'local_ada'),
        get_string('settings_timeout_desc', 'local_ada'),
        '30',
        PARAM_INT
    ));

    $settings->add(new admin_setting_configtext(
        'local_ada/allowedcategories',
        get_string('settings_allowedcategories', 'local_ada'),
        get_string('settings_allowedcategories_desc', 'local_ada'),
        '',
        PARAM_SEQUENCE
    ));
}

