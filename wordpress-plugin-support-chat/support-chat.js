(function(){
    const apiBase = (typeof SupportChatSettings !== 'undefined' && SupportChatSettings.apiBase) ? SupportChatSettings.apiBase.replace(/\/$/, '') : 'http://localhost:8000';

    function setCookie(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }

    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

    function registerEmail(email) {
        return fetch(apiBase + '/users/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email, role: 'client'})
        }).then(r => r.json());
    }

    function createTicket(email) {
        return fetch(apiBase + '/tickets/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email, role: 'client'})
        }).then(r => r.json());
    }

    function postMessage(email, ticket_id, content) {
        return fetch(apiBase + '/tickets/post-message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ticket_id: ticket_id, email: email, content: content})
        }).then(r => r.json());
    }

    function getMessages(ticket_id) {
        return fetch(apiBase + '/tickets/' + ticket_id + '/messages').then(r => r.json());
    }

    function appendMessage(container, msg) {
        var el = document.createElement('div');
        el.className = 'support-chat-message';
        var sender = 'System';
        if (msg.sender_id) sender = 'User';
        var text = msg.text || msg.content || JSON.stringify(msg);
        var ts = '';
        if (msg.created_at) {
            try { ts = ' (' + new Date(msg.created_at).toLocaleTimeString() + ')'; } catch(e) { ts = ''; }
        }
        el.textContent = sender + ': ' + text + ts;
        container.appendChild(el);
        container.scrollTop = container.scrollHeight;
        return el;
    }

    document.addEventListener('DOMContentLoaded', function(){
        console.log('Support Chat script loaded.');
        var root = document.getElementById('support-chat-root');
        var toggle = document.getElementById('support-chat-toggle');
        var emailInput = document.getElementById('support-chat-email');
        var registerBtn = document.getElementById('support-chat-register');
        var createTicketBtn = document.getElementById('support-chat-create-ticket');
        var sendBtn = document.getElementById('support-chat-send');
        var input = document.getElementById('support-chat-input');
        var messagesContainer = document.getElementById('support-chat-messages');

        // Start collapsed
        if (root) {
            root.classList.add('support-chat-collapsed');
            console.log('Support Chat initialized in collapsed state');
        } else {
            console.warn('Support Chat root element not found');
        }

        if (toggle) {
            toggle.addEventListener('click', function(){
                if (!root) return;
                root.classList.toggle('support-chat-collapsed');
                var ui = document.getElementById('support-chat-ui');
                if (ui) ui.setAttribute('aria-hidden', root.classList.contains('support-chat-collapsed') ? 'true' : 'false');
            });
        }
        // Also allow clicking the collapsed root area to open
        if (root) {
            root.addEventListener('click', function(e){
                // if clicked inside expanded UI, do nothing
                var isCollapsed = root.classList.contains('support-chat-collapsed');
                if (!isCollapsed) return;
                // if clicked on toggle element, let toggle handler run
                if (e.target && (e.target.id === 'support-chat-toggle' || e.target.closest('#support-chat-toggle'))) return;
                // open chat
                root.classList.remove('support-chat-collapsed');
                var uiOpen = document.getElementById('support-chat-ui');
                if (uiOpen) uiOpen.setAttribute('aria-hidden', 'false');
            });
        }

        var storedEmail = getCookie('support_chat_email');
        if (emailInput && storedEmail) {
            emailInput.value = storedEmail;
            var userElInit = document.getElementById('support-chat-user');
            if (userElInit) userElInit.textContent = storedEmail;
        }

        var currentTicketId = null;
        var pollInterval = null;

        function enableChatControls(enabled) {
            if (emailInput) emailInput.disabled = !enabled;
            if (registerBtn) registerBtn.disabled = !enabled;
            if (createTicketBtn) createTicketBtn.disabled = !enabled;
            if (input) input.disabled = !enabled;
            if (sendBtn) sendBtn.disabled = !enabled;
        }

        // Initially: allow entering email and registering, allow creating ticket after registration, but keep message input/send disabled until ticket exists
        if (input) input.disabled = true;
        if (sendBtn) sendBtn.disabled = true;

        if (registerBtn) {
            if (!emailInput) console.warn('Register button present but email input not found');
            registerBtn.addEventListener('click', function(){
                var email = emailInput ? emailInput.value.trim() : '';
                if (!email) {
                    alert('Please enter an email');
                    return;
                }
                registerEmail(email).then(function(result){
                    if (result.error) {
                        // could already exist, still set cookie
                        setCookie('support_chat_email', email, 7);
                        alert('Registered or exists. Email saved.');
                    } else if (result.message) {
                        setCookie('support_chat_email', email, 7);
                        alert(result.message);
                    } else {
                        setCookie('support_chat_email', email, 7);
                        alert('OK');
                    }
                        // After registration, show user and allow creating ticket
                        var userEl = document.getElementById('support-chat-user');
                        if (userEl) userEl.textContent = email;
                        if (createTicketBtn) createTicketBtn.disabled = false;
                }).catch(function(e){
                    alert('Network error: ' + e);
                });
            });
        } else {
            console.warn('Register button not found');
        }

        if (createTicketBtn) {
            createTicketBtn.addEventListener('click', function(){
                var email = getCookie('support_chat_email') || (emailInput ? emailInput.value.trim() : '');
                if (!email) { alert('Set email first'); return; }
                createTicket(email).then(function(result){
                    if (result.error) { alert('Error: ' + result.error); return; }
                    alert(result.message || 'Ticket created');
                    if (result.ticket_id) {
                        currentTicketId = result.ticket_id;
                        // enable message input
                        enableChatControls(true);
                        // explicitly remove readonly/disabled attributes and ensure pointer-events
                        if (input) {
                            try {
                                input.disabled = false;
                                input.readOnly = false;
                                input.removeAttribute && input.removeAttribute('disabled');
                                input.tabIndex = 0;
                                console.log('Support Chat: input enabled', input.disabled, input.readOnly);
                            } catch (e) { console.warn('Could not enable input', e); }
                        }
                        if (sendBtn) {
                            try { sendBtn.disabled = false; sendBtn.removeAttribute && sendBtn.removeAttribute('disabled'); } catch(e){}
                        }
                        var ui = document.getElementById('support-chat-ui');
                        if (ui) ui.style.pointerEvents = 'auto';
                        // ensure UI is visible and focus input
                        var ui = document.getElementById('support-chat-ui');
                        if (root) root.classList.remove('support-chat-collapsed');
                        if (ui) ui.setAttribute('aria-hidden', 'false');
                        if (input) { input.focus(); }
                        // load messages for new ticket
                        if (messagesContainer) messagesContainer.innerHTML = '';
                        getMessages(currentTicketId).then(function(res){
                            if (res.error) { console.warn(res.error); return; }
                            var msgs = res.messages || res;
                            if (Array.isArray(msgs) && messagesContainer) {
                                    messagesContainer.innerHTML = '';
                                    msgs.forEach(function(m){
                                        var el = appendMessage(messagesContainer, m);
                                        if (el) {
                                            var cls = 'incoming';
                                            var msgEmail = m.email || m.mail || null;
                                            var currentEmail = emailInput ? emailInput.value.trim() : storedEmail;
                                            if (msgEmail && currentEmail && msgEmail === currentEmail) cls = 'outgoing';
                                            el.classList.add(cls);
                                        }
                                    });
                                }
                        }).catch(function(e){ console.warn('Network error: ' + e); });

                        // start polling
                        if (pollInterval) clearInterval(pollInterval);
                        pollInterval = setInterval(function(){
                            if (!currentTicketId) return;
                            getMessages(currentTicketId).then(function(res){
                                if (res.error) { console.warn(res.error); return; }
                                var msgs = res.messages || res;
                                if (Array.isArray(msgs) && messagesContainer) {
                                    messagesContainer.innerHTML = '';
                                    msgs.forEach(function(m){
                                        var el = appendMessage(messagesContainer, m);
                                        if (el) {
                                            var cls = 'incoming';
                                            var msgEmail = m.email || m.mail || null;
                                            var currentEmail = emailInput ? emailInput.value.trim() : storedEmail;
                                            if (msgEmail && currentEmail && msgEmail === currentEmail) cls = 'outgoing';
                                            el.classList.add(cls);
                                        }
                                    });
                                }
                            }).catch(function(e){ console.warn('Network error: ' + e); });
                        }, 3000);
                    }
                }).catch(function(e){ alert('Network error: ' + e); });
            });
        } else {
            console.warn('Create ticket button not found');
        }

        if (sendBtn) {
            sendBtn.addEventListener('click', function(){
                var email = getCookie('support_chat_email') || (emailInput ? emailInput.value.trim() : '');
                if (!email) { alert('Set email first'); return; }
                var text = input ? input.value.trim() : '';
                console.log('Support Chat: send clicked, input value:', text, 'disabled:', input ? input.disabled : 'no-input');
                if (!text) { return; }
                if (!currentTicketId) {
                    alert('Create a ticket first');
                    return;
                }
                postMessage(email, currentTicketId, text).then(function(result){
                    if (result.error) { alert('Error: ' + result.error); return; }
                    // Append local message
                    if (messagesContainer) appendMessage(messagesContainer, {sender_id: 1, text: text});
                    if (input) input.value = '';
                }).catch(function(e){ alert('Network error: ' + e); });
            });
        } else {
            console.warn('Send button not found');
        }

        // For demo: allow opening ticket id by clicking message area
        if (messagesContainer) {
            messagesContainer.addEventListener('dblclick', function(){
                var ticket = prompt('Enter ticket id to load messages');
                if (!ticket) return;
                currentTicketId = parseInt(ticket, 10);
                messagesContainer.innerHTML = '';
                getMessages(currentTicketId).then(function(res){
                    if (res.error) { alert('Error: ' + res.error); return; }
                    var msgs = res.messages || res;
                    if (Array.isArray(msgs)) {
                        msgs.forEach(function(m){ appendMessage(messagesContainer, m); });
                    }
                }).catch(function(e){ alert('Network error: ' + e); });
            });
        } else {
            console.warn('Messages container not found');
        }
        // Close button behavior
        var closeBtn = document.getElementById('support-chat-close');
        if (closeBtn && root) {
            closeBtn.addEventListener('click', function(e){
                e.stopPropagation();
                root.classList.add('support-chat-collapsed');
            });
        }
    });
})();
