<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

/**
 * Spanish language strings for local_ada.
 *
 * @package    local_ada
 * @copyright  2026 Juan Luis Fernandez Abreu (UCV)
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

$string['pluginname'] = 'Asistente ADA';
$string['ada:use'] = 'Usar el asistente docente ADA';
$string['settings_middlewareurl'] = 'URL del Middleware';
$string['settings_middlewareurl_desc'] = 'URL base del Middleware externo de ADA (ej. http://host.docker.internal:8000).';
$string['settings_servicetoken'] = 'Token de servicio';
$string['settings_servicetoken_desc'] = 'Secreto compartido (X-ADA-Token) configurado en el archivo .env del Middleware.';
$string['settings_timeout'] = 'Tiempo de espera (segundos)';
$string['settings_timeout_desc'] = 'Tiempo máximo de espera para las respuestas de inferencia del Middleware.';
$string['workspace_title'] = 'ADA — Asistente Docente';
$string['workspace_subtitle'] = 'Genera preguntas de opción múltiple en formato Moodle XML para su revisión e importación manual en el Banco de preguntas.';
$string['field_topic'] = 'Tema o contenido base';
$string['field_topic_placeholder'] = 'Ej.: Complejidad algorítmica (notación Big-O) y árboles binarios de búsqueda...';
$string['field_count'] = 'Cantidad de preguntas';
$string['field_difficulty'] = 'Nivel de dificultad';
$string['difficulty_basic'] = 'Básico';
$string['difficulty_intermediate'] = 'Intermedio';
$string['difficulty_advanced'] = 'Avanzado';
$string['field_provider'] = 'Proveedor de IA';
$string['provider_auto'] = 'Automático (Primario + Fallback)';
$string['btn_generate'] = 'Generar preguntas';
$string['btn_download_xml'] = 'Descargar Moodle XML';
$string['generating'] = 'Generando y validando preguntas...';
$string['preview_title'] = 'Vista previa antes de importar';
$string['error_middleware_unconfigured'] = 'La URL o el token del Middleware de ADA no están configurados en la administración del sitio.';
$string['error_middleware_http'] = 'Error al comunicarse con el Middleware de ADA (HTTP {$a}).';

