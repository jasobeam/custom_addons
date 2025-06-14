# -*- coding: utf-8 -*-:
import urllib.parse
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    user_access_token = fields.Char(string="Facebook Access Token", config_parameter="gl_facebook.api_key")
    facebook_app_id = fields.Char(string="Facebook API Key", config_parameter="gl_facebook.app_id")
    facebook_app_secret = fields.Char(string="Facebook APP Secret", config_parameter="gl_facebook.secret")
    facebook_redirect_uri = fields.Char(string="Facebook Redirect URI", config_parameter="facebook_redirect", default="http://localhost:8018/facebook-auth/")

    aws_access_key = fields.Char(string="AWS Clave de acceso", config_parameter="gl_aws.api_key")
    aws_secret = fields.Char(string="AWS Clave de acceso secreta", config_parameter="gl_aws.secret")

    tiktok_client = fields.Char(string="TikTok Clave de cliente", config_parameter="tiktok_key")
    tiktok_secret = fields.Char(string="TikTok Clave secreta", config_parameter="tiktok_secret")
    tiktok_redirect_uri = fields.Char(string="TikTok Redirect URI", config_parameter="tiktok_redirect", default="http://localhost:8018/tiktok-auth/")

    google_developer_token = fields.Char(string="Google Developer Token", config_parameter="gl_google.developer_token")
    google_client_id = fields.Char(string="Google Client ID", config_parameter="gl_google.client_id")
    google_client_secret = fields.Char(string="Google Client Secret", config_parameter="gl_google.client_secret")
    google_redirect_uri = fields.Char(string="Google Redirect URI", config_parameter="gl_google.redirect_uri", default="http://localhost:8018/google-auth/")
    google_access_token = fields.Char("Google Access Token", config_parameter="gl_google.access_token")
    google_refresh_token = fields.Char("Google Refresh Token", config_parameter="gl_google.refresh_token")
    google_login_customer_id = fields.Char(string="Google Ads Manager Account (Login Customer ID)", config_parameter="gl_google.login_customer_id")

    linkedin_client_id = fields.Char("LinkedIn Client ID", config_parameter="linkedin.client_id")
    linkedin_client_secret = fields.Char("LinkedIn Client Secret", config_parameter="linkedin.client_secret")
    linkedin_redirect_uri = fields.Char("Redirect URI", config_parameter="linkedin.redirect_uri")
    linkedin_access_token = fields.Char(string="LinkedIn Access Token", config_parameter='linkedin.access_token')
    linkedin_token_expiry = fields.Char(string="Token Expiry", config_parameter='linkedin.token_expiry')

    def conectar_facebook(self):
        scopes_list = [
            "pages_read_user_content",
            "ads_read",
            "ads_management",
            "publish_video",
            "business_management",
            "pages_show_list",
            "instagram_basic",
            "instagram_content_publish",
            "pages_read_engagement",
            "pages_manage_posts",
            "public_profile",
            "read_insights",
            "instagram_manage_insights"
        ]

        scopes = ",".join(scopes_list)

        auth_url = (f"https://www.facebook.com/v22.0/dialog/oauth"
                    f"?client_id={self.facebook_app_id}"
                    f"&redirect_uri={self.facebook_redirect_uri}"
                    f"&scope={scopes}")

        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }

    def conectar_google(self):
        scopes_list = [
            "https://www.googleapis.com/auth/adwords",
            "https://www.googleapis.com/auth/webmasters.readonly",
            "https://www.googleapis.com/auth/analytics.readonly",
        ]

        scopes = " ".join(scopes_list)

        auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth"
                    f"?client_id={self.google_client_id}"
                    f"&redirect_uri={self.google_redirect_uri}"
                    f"&response_type=code"
                    f"&scope={scopes}"
                    f"&access_type=offline"
                    f"&prompt=consent")

        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }

    def conectar_linkedin(self):
        self.ensure_one()

        # 1. Configuración base
        base_url = "https://www.linkedin.com/oauth/v2/authorization"
        client_id = self.env['ir.config_parameter'].sudo().get_param("linkedin.client_id")
        redirect_uri = self.env['ir.config_parameter'].sudo().get_param("linkedin.redirect_uri")

        # 2. Scopes actualizados (2024)
        scope = [
            "w_member_social",
            "w_organization_social",
            "r_organization_admin",
            "rw_organization_admin"
        ]

        # 3. Parámetros de la solicitud
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(scope),  # Espacios normales (urlencode se encargará)
        }

        # 4. Construcción de la URL con codificación correcta
        query_string = urllib.parse.urlencode(params, safe='', quote_via=urllib.parse.quote)
        url = f"{base_url}?{query_string}"

        # 6. Retorno de la acción
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'  # 'new' es mejor que 'blank' para Odoo
        }
