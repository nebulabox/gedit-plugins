/*
 * Copyright (C) 2008-2014 Ignacio Casal Quinteiro <icq@gnome.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "gedit-drawspaces-app-activatable.h"

#include <gedit/gedit-app.h>
#include <gedit/gedit-app-activatable.h>
#include <gedit/gedit-debug.h>
#include <libpeas/peas-object-module.h>
#include <gio/gio.h>
#include <glib/gi18n-lib.h>

struct _GeditDrawspacesAppActivatablePrivate
{
	GeditApp *app;
	GeditMenuExtension *menu_ext;
};

enum
{
	PROP_0,
	PROP_APP
};

static void gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (GeditDrawspacesAppActivatable,
				gedit_drawspaces_app_activatable,
				G_TYPE_OBJECT,
				0,
				G_ADD_PRIVATE_DYNAMIC (GeditDrawspacesAppActivatable)
				G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_APP_ACTIVATABLE,
							       gedit_app_activatable_iface_init))

static void
gedit_drawspaces_app_activatable_dispose (GObject *object)
{
	GeditDrawspacesAppActivatable *activatable = GEDIT_DRAWSPACES_APP_ACTIVATABLE (object);
	GeditDrawspacesAppActivatablePrivate *priv = gedit_drawspaces_app_activatable_get_instance_private (activatable);

	g_clear_object (&priv->app);

	G_OBJECT_CLASS (gedit_drawspaces_app_activatable_parent_class)->dispose (object);
}

static void
gedit_drawspaces_app_activatable_set_property (GObject      *object,
                                               guint         prop_id,
                                               const GValue *value,
                                               GParamSpec   *pspec)
{
	GeditDrawspacesAppActivatable *activatable = GEDIT_DRAWSPACES_APP_ACTIVATABLE (object);
	GeditDrawspacesAppActivatablePrivate *priv = gedit_drawspaces_app_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_APP:
			priv->app = GEDIT_APP (g_value_dup_object (value));
			break;
		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_drawspaces_app_activatable_get_property (GObject    *object,
                                               guint       prop_id,
                                               GValue     *value,
                                               GParamSpec *pspec)
{
	GeditDrawspacesAppActivatable *activatable = GEDIT_DRAWSPACES_APP_ACTIVATABLE (object);
	GeditDrawspacesAppActivatablePrivate *priv = gedit_drawspaces_app_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_APP:
			g_value_set_object (value, priv->app);
			break;
		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_drawspaces_app_activatable_class_init (GeditDrawspacesAppActivatableClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	object_class->dispose = gedit_drawspaces_app_activatable_dispose;
	object_class->set_property = gedit_drawspaces_app_activatable_set_property;
	object_class->get_property = gedit_drawspaces_app_activatable_get_property;

	g_object_class_override_property (object_class, PROP_APP, "app");
}

static void
gedit_drawspaces_app_activatable_class_finalize (GeditDrawspacesAppActivatableClass *klass)
{
}

static void
gedit_drawspaces_app_activatable_init (GeditDrawspacesAppActivatable *self)
{
}

static void
gedit_drawspaces_app_activatable_activate (GeditAppActivatable *activatable)
{
	GeditDrawspacesAppActivatable *app_activatable = GEDIT_DRAWSPACES_APP_ACTIVATABLE (activatable);
	GeditDrawspacesAppActivatablePrivate *priv = gedit_drawspaces_app_activatable_get_instance_private (app_activatable);
	GMenuItem *item;

	gedit_debug (DEBUG_PLUGINS);

	priv->menu_ext = gedit_app_activatable_extend_menu (activatable, "view-section-2");
	item = g_menu_item_new (_("Show _White Space"), "win.show-white-space");
	gedit_menu_extension_append_menu_item (priv->menu_ext, item);
	g_object_unref (item);
}

static void
gedit_drawspaces_app_activatable_deactivate (GeditAppActivatable *activatable)
{
	GeditDrawspacesAppActivatable *app_activatable = GEDIT_DRAWSPACES_APP_ACTIVATABLE (activatable);
	GeditDrawspacesAppActivatablePrivate *priv = gedit_drawspaces_app_activatable_get_instance_private (app_activatable);

	gedit_debug (DEBUG_PLUGINS);

	g_clear_object (&priv->menu_ext);
}

static void
gedit_app_activatable_iface_init (GeditAppActivatableInterface *iface)
{
	iface->activate = gedit_drawspaces_app_activatable_activate;
	iface->deactivate = gedit_drawspaces_app_activatable_deactivate;
}

void
gedit_drawspaces_app_activatable_register (GTypeModule *module)
{
	gedit_drawspaces_app_activatable_register_type (module);

	peas_object_module_register_extension_type (PEAS_OBJECT_MODULE (module),
	                                            GEDIT_TYPE_APP_ACTIVATABLE,
	                                            GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE);
}

/* ex:set ts=8 noet: */
