<?php
/**
 * Plugin Name: Support Chat Bridge
 * Description: Lightweight support chat frontend that talks to external FastAPI backend.
 * Version: 0.1
 * Author: Generated
 */

if (!defined('ABSPATH')) {
    exit;
}

class SupportChatPlugin {
    private $option_name = 'support_chat_api_base';

    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'settings_init'));
        add_action('wp_footer', array($this, 'render_widget_footer'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('support_chat_widget', array($this, 'render_widget'));
    }

    public function render_widget_footer() {
        echo $this->render_widget();
    }

    public function add_admin_menu() {
        add_options_page('Support Chat', 'Support Chat', 'manage_options', 'support_chat', array($this, 'options_page'));
    }

    public function settings_init() {
        register_setting('support_chat_group', $this->option_name);
        add_settings_section('support_chat_section', 'Support Chat Settings', null, 'support_chat');
        add_settings_field($this->option_name, 'API Base URL', array($this, 'api_field_render'), 'support_chat', 'support_chat_section');
    }

    public function api_field_render() {
        $value = get_option($this->option_name, 'http://localhost:8000');
        echo "<input type='text' id='support_chat_api_base' name='{$this->option_name}' value='{$value}' style='width: 400px;' />";
    }

    public function options_page() {
        ?>
        <form action='options.php' method='post'>
            <h2>Support Chat</h2>
            <?php
            settings_fields('support_chat_group');
            do_settings_sections('support_chat');
            submit_button();
            ?>
        </form>
        <?php
    }

    public function enqueue_scripts() {
        $plugin_url = plugin_dir_url(__FILE__);
        wp_register_script('support_chat_js', $plugin_url . 'support-chat.js', array('jquery'), '0.1', true);
        wp_localize_script('support_chat_js', 'SupportChatSettings', array(
            'apiBase' => get_option($this->option_name, 'http://localhost:8000')
        ));
        wp_enqueue_script('support_chat_js');
        wp_enqueue_style('support_chat_css', $plugin_url . 'support-chat.css');
    }

    public function render_widget($atts = array()) {
        ob_start();
        ?>
        <div id="support-chat-root" class="support-chat-root support-chat-collapsed">
            <div id="support-chat-toggle" class="support-chat-toggle" aria-label="Open support chat">💬</div>
            <div id="support-chat-ui" class="support-chat-ui" role="dialog" aria-hidden="true">
                <div id="support-chat-header" class="support-chat-header">
                    <div class="support-chat-title">Support</div>
                    <div class="support-chat-controls">
                        <span id="support-chat-user" class="support-chat-user">Not signed</span>
                        <button id="support-chat-close" class="support-chat-close" aria-label="Close">✕</button>
                    </div>
                </div>
                <div id="support-chat-body" class="support-chat-body">
                    <div id="support-chat-messages" class="support-chat-messages"></div>
                </div>
                <div id="support-chat-footer" class="support-chat-footer">
                    <div class="support-chat-row">
                        <input type="email" id="support-chat-email" class="support-chat-email" placeholder="Enter your email" />
                        <button id="support-chat-register" class="support-chat-btn">Register</button>
                    </div>
                    <div class="support-chat-row">
                        <button id="support-chat-create-ticket" class="support-chat-btn">Create Ticket</button>
                    </div>
                    <div class="support-chat-row support-chat-compose">
                        <input type="text" id="support-chat-input" class="support-chat-input" placeholder="Type a message..." />
                        <button id="support-chat-send" class="support-chat-send">Send</button>
                    </div>
                </div>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }
}

new SupportChatPlugin();
