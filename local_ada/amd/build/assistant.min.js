define(['core/ajax', 'core/notification'], function(Ajax, Notification) {
    'use strict';

    var lastContent = '';
    var lastFilename = 'ada_preguntas.xml';
    var lastMime = 'application/xml;charset=utf-8';

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str || ''));
        return div.innerHTML;
    }

    function renderPreview(questions) {
        var container = document.getElementById('ada-preview-list');
        container.innerHTML = '';
        questions.forEach(function(q, idx) {
            var item = document.createElement('div');
            item.className = 'list-group-item';
            var optionsHtml = (q.options || []).map(function(opt) {
                var badge = opt.fraction === 100 ? ' <span class="badge bg-success">Correcta</span>' : '';
                return '<li>' + escapeHtml(opt.text) + badge + '</li>';
            }).join('');
            item.innerHTML =
                '<div class="fw-bold mb-1">' + (idx + 1) + '. ' + escapeHtml(q.name) + '</div>' +
                '<p class="mb-2">' + escapeHtml(q.question_text) + '</p>' +
                '<ul class="mb-0">' + optionsHtml + '</ul>';
            container.appendChild(item);
        });
    }

    return {
        init: function(courseid) {
            var form = document.getElementById('ada-question-form');
            var btn = document.getElementById('ada-generate-btn');
            var status = document.getElementById('ada-status');
            var errorBox = document.getElementById('ada-error');
            var resultBox = document.getElementById('ada-result');
            var metaBox = document.getElementById('ada-meta');
            var downloadBtn = document.getElementById('ada-download-btn');

            if (!form) {
                return;
            }

            downloadBtn.addEventListener('click', function() {
                if (!lastContent) {
                    return;
                }
                var blob = new Blob([lastContent], {type: lastMime});
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = lastFilename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            });

            form.addEventListener('submit', function(e) {
                e.preventDefault();
                var topic = document.getElementById('ada-topic').value.trim();
                if (!topic) {
                    return;
                }
                var exportFormat = document.getElementById('ada-format').value;

                btn.disabled = true;
                status.classList.remove('d-none');
                errorBox.classList.add('d-none');
                resultBox.classList.add('d-none');

                Ajax.call([{
                    methodname: 'local_ada_generate_questions',
                    args: {
                        courseid: courseid,
                        topic: topic,
                        count: parseInt(document.getElementById('ada-count').value, 10),
                        difficulty: document.getElementById('ada-difficulty').value,
                        provider: document.getElementById('ada-provider').value,
                        exportformat: exportFormat
                    }
                }])[0].then(function(res) {
                    lastContent = res.exportedcontent || '';
                    lastFilename = res.filename || 'ada_preguntas.xml';
                    lastMime = exportFormat === 'gift' ? 'text/plain;charset=utf-8' : 'application/xml;charset=utf-8';
                    downloadBtn.textContent = exportFormat === 'gift' ? 'Descargar GIFT (.txt)' : 'Descargar Moodle XML';
                    var questions = JSON.parse(res.questionsjson || '[]');
                    renderPreview(questions);
                    metaBox.textContent = 'Proveedor: ' + res.providerused +
                        ' (' + res.modelused + ') · Latencia: ' + res.latencyms + ' ms';
                    resultBox.classList.remove('d-none');
                }).catch(function(err) {
                    errorBox.textContent = (err && err.message)
                        ? err.message
                        : 'El asistente no pudo responder en este momento. Inténtalo nuevamente.';
                    errorBox.classList.remove('d-none');
                }).finally(function() {
                    btn.disabled = false;
                    status.classList.add('d-none');
                });
            });
        }
    };
});

