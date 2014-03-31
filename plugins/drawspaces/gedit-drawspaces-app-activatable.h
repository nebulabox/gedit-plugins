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

#ifndef __GEDIT_DRAWSPACES_APP_ACTIVATABLE_H__
#define __GEDIT_DRAWSPACES_APP_ACTIVATABLE_H__

#include <glib-object.h>

G_BEGIN_DECLS

#define GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE			(gedit_drawspaces_app_activatable_get_type ())
#define GEDIT_DRAWSPACES_APP_ACTIVATABLE(obj)			(G_TYPE_CHECK_INSTANCE_CAST ((obj), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE, GeditDrawspacesAppActivatable))
#define GEDIT_DRAWSPACES_APP_ACTIVATABLE_CONST(obj)		(G_TYPE_CHECK_INSTANCE_CAST ((obj), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE, GeditDrawspacesAppActivatable const))
#define GEDIT_DRAWSPACES_APP_ACTIVATABLE_CLASS(klass)		(G_TYPE_CHECK_CLASS_CAST ((klass), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE, GeditDrawspacesAppActivatableClass))
#define GEDIT_IS_DRAWSPACES_APP_ACTIVATABLE(obj)		(G_TYPE_CHECK_INSTANCE_TYPE ((obj), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE))
#define GEDIT_IS_DRAWSPACES_APP_ACTIVATABLE_CLASS(klass)	(G_TYPE_CHECK_CLASS_TYPE ((klass), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE))
#define GEDIT_DRAWSPACES_APP_ACTIVATABLE_GET_CLASS(obj)		(G_TYPE_INSTANCE_GET_CLASS ((obj), GEDIT_TYPE_DRAWSPACES_APP_ACTIVATABLE, GeditDrawspacesAppActivatableClass))

typedef struct _GeditDrawspacesAppActivatable		GeditDrawspacesAppActivatable;
typedef struct _GeditDrawspacesAppActivatableClass	GeditDrawspacesAppActivatableClass;
typedef struct _GeditDrawspacesAppActivatablePrivate	GeditDrawspacesAppActivatablePrivate;

struct _GeditDrawspacesAppActivatable
{
	GObject parent;

	GeditDrawspacesAppActivatablePrivate *priv;
};

struct _GeditDrawspacesAppActivatableClass
{
	GObjectClass parent_class;
};

GType          gedit_drawspaces_app_activatable_get_type   (void) G_GNUC_CONST;

void           gedit_drawspaces_app_activatable_register   (GTypeModule *module);

G_END_DECLS

#endif /* __GEDIT_DRAWSPACES_APP_ACTIVATABLE_H__ */
