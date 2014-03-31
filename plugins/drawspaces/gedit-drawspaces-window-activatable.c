/*
 * Copyright (C) 2008-2014 Ignacio Casal Quinteiro <nacho.resa@gmail.com>
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

#include "gedit-drawspaces-window-activatable.h"
#include "gedit-drawspaces-view-activatable.h"

#include <glib/gi18n-lib.h>
#include <gedit/gedit-debug.h>
#include <gedit/gedit-view.h>
#include <gedit/gedit-tab.h>
#include <gedit/gedit-window.h>
#include <gedit/gedit-window-activatable.h>
#include <libpeas/peas-object-module.h>

typedef struct _GeditDrawspacesWindowActivatablePrivate
{
	GSettings *settings;
	GeditWindow *window;
} GeditDrawspacesWindowActivatablePrivate;

enum
{
	PROP_0,
	PROP_WINDOW
};

static void gedit_window_activatable_iface_init (GeditWindowActivatableInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (GeditDrawspacesWindowActivatable,
				gedit_drawspaces_window_activatable,
				G_TYPE_OBJECT,
				0,
				G_ADD_PRIVATE_DYNAMIC (GeditDrawspacesWindowActivatable)
				G_IMPLEMENT_INTERFACE_DYNAMIC (GEDIT_TYPE_WINDOW_ACTIVATABLE,
							       gedit_window_activatable_iface_init))

static void
gedit_drawspaces_window_activatable_init (GeditDrawspacesWindowActivatable *activatable)
{
}

static void
gedit_drawspaces_window_activatable_dispose (GObject *object)
{
	GeditDrawspacesWindowActivatable *activatable = GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE (object);
	GeditDrawspacesWindowActivatablePrivate *priv = gedit_drawspaces_window_activatable_get_instance_private (activatable);

	gedit_debug_message (DEBUG_PLUGINS, "GeditDrawspacesWindowActivatable disposing");

	g_clear_object (&priv->window);

	G_OBJECT_CLASS (gedit_drawspaces_window_activatable_parent_class)->dispose (object);
}

static void
gedit_drawspaces_window_activatable_set_property (GObject      *object,
                                                  guint         prop_id,
                                                  const GValue *value,
                                                  GParamSpec   *pspec)
{
	GeditDrawspacesWindowActivatable *activatable = GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE (object);
	GeditDrawspacesWindowActivatablePrivate *priv = gedit_drawspaces_window_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_WINDOW:
			priv->window = GEDIT_WINDOW (g_value_dup_object (value));
			break;
		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_drawspaces_window_activatable_get_property (GObject    *object,
                                                  guint       prop_id,
                                                  GValue     *value,
                                                  GParamSpec *pspec)
{
	GeditDrawspacesWindowActivatable *activatable = GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE (object);
	GeditDrawspacesWindowActivatablePrivate *priv = gedit_drawspaces_window_activatable_get_instance_private (activatable);

	switch (prop_id)
	{
		case PROP_WINDOW:
			g_value_set_object (value, priv->window);
			break;
		default:
			G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
			break;
	}
}

static void
gedit_drawspaces_window_activatable_window_activate (GeditWindowActivatable *activatable)
{
	GeditDrawspacesWindowActivatablePrivate *priv;
	GAction *action;

	gedit_debug (DEBUG_PLUGINS);

	priv = gedit_drawspaces_window_activatable_get_instance_private (GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE (activatable));
	priv->settings = g_settings_new (DRAWSPACES_SETTINGS_BASE);

	action = g_settings_create_action (priv->settings,
	                                   SETTINGS_KEY_SHOW_WHITE_SPACE);
	g_action_map_add_action (G_ACTION_MAP (priv->window),
	                         action);
	g_object_unref (action);
}

static void
gedit_drawspaces_window_activatable_window_deactivate (GeditWindowActivatable *activatable)
{
	GeditDrawspacesWindowActivatablePrivate *priv;

	gedit_debug (DEBUG_PLUGINS);

	priv = gedit_drawspaces_window_activatable_get_instance_private (GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE (activatable));

	g_action_map_remove_action (G_ACTION_MAP (priv->window),
	                            SETTINGS_KEY_SHOW_WHITE_SPACE);

	g_clear_object (&priv->settings);
}

static void
gedit_drawspaces_window_activatable_class_init (GeditDrawspacesWindowActivatableClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	object_class->dispose = gedit_drawspaces_window_activatable_dispose;
	object_class->set_property = gedit_drawspaces_window_activatable_set_property;
	object_class->get_property = gedit_drawspaces_window_activatable_get_property;

	g_object_class_override_property (object_class, PROP_WINDOW, "window");
}

static void
gedit_drawspaces_window_activatable_class_finalize (GeditDrawspacesWindowActivatableClass *klass)
{
}

static void
gedit_window_activatable_iface_init (GeditWindowActivatableInterface *iface)
{
	iface->activate = gedit_drawspaces_window_activatable_window_activate;
	iface->deactivate = gedit_drawspaces_window_activatable_window_deactivate;
}

void
gedit_drawspaces_window_activatable_register (GTypeModule *module)
{
	gedit_drawspaces_window_activatable_register_type (module);

	peas_object_module_register_extension_type (PEAS_OBJECT_MODULE (module),
						    GEDIT_TYPE_WINDOW_ACTIVATABLE,
						    GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE);
}

/* ex:set ts=8 noet: */
