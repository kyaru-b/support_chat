Support Chat Bridge WordPress plugin

Installation:
- Copy the `wordpress-plugin-support-chat` folder into `wp-content/plugins/`.
- Activate the plugin in WordPress admin.
- Go to Settings → Support Chat and set the API Base URL (e.g., http://localhost:8000).
- Place the shortcode [support_chat_widget] in a page to show the widget.

Usage:
- Enter an email and click `Register / Set Email` (will POST to `/users/create`).
- Click `Create Ticket` to call `/tickets/create`.
- Double-click the messages area to enter ticket id to load messages (`GET /tickets/{id}/messages`).
- Type a message and click `Send` to POST `/tickets/post-message`.

Notes:
- The backend in this workspace exposes endpoints in `src/routers/`.
- The plugin stores the email in a cookie `support_chat_email` for 7 days.
- The backend should be running and accessible from the WordPress host. CORS may need to be enabled on the FastAPI app.
