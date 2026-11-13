define(['core/ajax'], function(Ajax) {
    'use strict';

    var MAX_HISTORY = 20;

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

    function loadHistory(key) {
        try {
            var raw = sessionStorage.getItem(key);
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            return [];
        }
    }

    function saveHistory(key, items) {
        try {
            sessionStorage.setItem(key, JSON.stringify(items.slice(-MAX_HISTORY)));
        } catch (e) {
            // Ignore storage quota errors.
        }
    }

    return {
        init: function(courseid) {
            var toggleBtn = document.getElementById('ada-chat-toggle');
            var closeBtn = document.getElementById('ada-chat-close');
            var clearBtn = document.getElementById('ada-chat-clear');
            var drawer = document.getElementById('ada-chat-drawer');
            var messages = document.getElementById('ada-chat-messages');
            var form = document.getElementById('ada-chat-form');
            var input = document.getElementById('ada-chat-input');
            var sendBtn = document.getElementById('ada-chat-send');

            if (!toggleBtn || !drawer || !form) {
                return;
            }

            var historyKey = 'ada_chat_history_' + courseid;
            var history = loadHistory(historyKey);
            var welcomeHtml = messages.innerHTML;

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

            var appendBubble = function(html, isUser) {
                var div = document.createElement('div');
                div.className = 'ada-msg ' + (isUser ? 'ada-msg-user' : 'ada-msg-bot');
                div.innerHTML = html;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
                return div;
            };

            var renderResultIntoBubble = function(bubble, entry) {
                var questions = entry.questions || [];
                var listHtml = questions.map(function(q, idx) {
                    return '<div class="mb-1"><strong>' + (idx + 1) + '.</strong> ' + escapeHtml(q.name) + '</div>';
                }).join('');

                bubble.innerHTML =
                    '<div class="mb-2">' + listHtml + '</div>' +
                    '<div class="small text-muted mb-2">' +
                        escapeHtml(entry.providerused) + ' · ' + entry.latencyms + ' ms' +
                    '</div>' +
                    '<button type="button" class="btn btn-success btn-sm ada-dl-btn">' +
                        escapeHtml(entry.label) +
                    '</button>';

                var dlBtn = bubble.querySelector('.ada-dl-btn');
                dlBtn.addEventListener('click', function() {
                    downloadFile(entry.exportedcontent || '', entry.filename || 'ada_preguntas.xml', entry.mime);
                });
            };

            history.forEach(function(item) {
                if (item.role === 'user') {
                    appendBubble(escapeHtml(item.text), true);
                } else if (item.role === 'error') {
                    appendBubble('<span class="text-danger">' + escapeHtml(item.text) + '</span>', false);
                } else if (item.role === 'bot') {
                    var b = appendBubble('', false);
                    renderResultIntoBubble(b, item);
                }
            });

            if (clearBtn) {
                clearBtn.addEventListener('click', function() {
                    history = [];
                    saveHistory(historyKey, history);
                    messages.innerHTML = welcomeHtml;
                });
            }

            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    form.requestSubmit();
                }
            });

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
                history.push({role: 'user', text: topic});
                saveHistory(historyKey, history);

                input.value = '';
                sendBtn.disabled = true;

                var loadingBubble = appendBubble('<em>Generando y validando preguntas...</em>', false);

                Promise.resolve(Ajax.call([{
                    methodname: 'local_ada_generate_questions',
                    args: {
                        courseid: courseid,
                        topic: topic,
                        count: count,
                        difficulty: difficulty,
                        provider: provider,
                        exportformat: exportFormat
                    }
                }])[0]).then(function(res) {
                    var questions = JSON.parse(res.questionsjson || '[]');
                    var mime = exportFormat === 'gift' ? 'text/plain;charset=utf-8' : 'application/xml;charset=utf-8';
                    var label = exportFormat === 'gift' ? 'Descargar GIFT (.txt)' : 'Descargar Moodle XML';

                    var entry = {
                        role: 'bot',
                        questions: questions,
                        providerused: res.providerused,
                        latencyms: res.latencyms,
                        exportedcontent: res.exportedcontent || '',
                        filename: res.filename || 'ada_preguntas.xml',
                        mime: mime,
                        label: label
                    };
                    renderResultIntoBubble(loadingBubble, entry);
                    history.push(entry);
                    saveHistory(historyKey, history);
                }).catch(function(err) {
                    var msg = (err && err.message) ? err.message : 'Error al generar preguntas.';
                    loadingBubble.innerHTML = '<span class="text-danger">' + escapeHtml(msg) + '</span>';
                    history.push({role: 'error', text: msg});
                    saveHistory(historyKey, history);
                }).finally(function() {
                    sendBtn.disabled = false;
                });
            });
        }
    };
});
