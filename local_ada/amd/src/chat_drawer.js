define(['core/ajax'], function(Ajax) {
    'use strict';

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str || ''));
        return div.innerHTML;
    }

    function downloadFile(content, filename, mime) {
        var blob = new Blob([content], {type: mime});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    return {
        init: function(courseid) {
            var toggleBtn = document.getElementById('ada-chat-toggle');
            var closeBtn = document.getElementById('ada-chat-close');
            var drawer = document.getElementById('ada-chat-drawer');
            var messages = document.getElementById('ada-chat-messages');
            var form = document.getElementById('ada-chat-form');
            var input = document.getElementById('ada-chat-input');
            var sendBtn = document.getElementById('ada-chat-send');

            if (!toggleBtn || !drawer || !form) {
                return;
            }

            var setOpen = function(open) {
                drawer.classList.toggle('ada-open', open);
                drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
                try {
                    sessionStorage.setItem('ada_drawer_open', open ? '1' : '0');
                } catch (e) {
                    // Ignore storage restrictions.
                }
            };

            try {
                if (sessionStorage.getItem('ada_drawer_open') === '1') {
                    setOpen(true);
                }
            } catch (e) {
                // Ignore.
            }

            toggleBtn.addEventListener('click', function() {
                setOpen(!drawer.classList.contains('ada-open'));
            });
            closeBtn.addEventListener('click', function() {
                setOpen(false);
            });

            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    form.requestSubmit();
                }
            });

            var appendBubble = function(html, isUser) {
                var div = document.createElement('div');
                div.className = 'ada-msg ' + (isUser ? 'ada-msg-user' : 'ada-msg-bot');
                div.innerHTML = html;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
                return div;
            };

            form.addEventListener('submit', function(e) {
                e.preventDefault();
                var topic = input.value.trim();
                if (!topic) {
                    return;
                }

                var count = parseInt(document.getElementById('ada-chat-count').value, 10);
                var difficulty = document.getElementById('ada-chat-diff').value;
                var exportFormat = document.getElementById('ada-chat-format').value;
                var provider = document.getElementById('ada-chat-provider').value;

                appendBubble(escapeHtml(topic), true);
                input.value = '';
                sendBtn.disabled = true;

                var loadingBubble = appendBubble('<em>Generando y validando preguntas...</em>', false);

                Ajax.call([{
                    methodname: 'local_ada_generate_questions',
                    args: {
                        courseid: courseid,
                        topic: topic,
                        count: count,
                        difficulty: difficulty,
                        provider: provider,
                        exportformat: exportFormat
                    }
                }])[0].then(function(res) {
                    var questions = JSON.parse(res.questionsjson || '[]');
                    var listHtml = questions.map(function(q, idx) {
                        return '<div class="mb-1"><strong>' + (idx + 1) + '.</strong> ' + escapeHtml(q.name) + '</div>';
                    }).join('');

                    var mime = exportFormat === 'gift' ? 'text/plain;charset=utf-8' : 'application/xml;charset=utf-8';
                    var label = exportFormat === 'gift' ? 'Descargar GIFT (.txt)' : 'Descargar Moodle XML';

                    loadingBubble.innerHTML =
                        '<div class="mb-2">' + listHtml + '</div>' +
                        '<div class="small text-muted mb-2">' +
                            escapeHtml(res.providerused) + ' · ' + res.latencyms + ' ms' +
                        '</div>' +
                        '<button type="button" class="btn btn-success btn-sm ada-dl-btn">' + label + '</button>';

                    var dlBtn = loadingBubble.querySelector('.ada-dl-btn');
                    dlBtn.addEventListener('click', function() {
                        downloadFile(res.exportedcontent || '', res.filename || 'ada_preguntas.xml', mime);
                    });
                }).catch(function(err) {
                    loadingBubble.innerHTML =
                        '<span class="text-danger">' + escapeHtml(err.message || 'Error al generar preguntas.') + '</span>';
                }).finally(function() {
                    sendBtn.disabled = false;
                });
            });
        }
    };
});

