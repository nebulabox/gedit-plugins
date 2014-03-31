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
 *
 * $Id: gedit-drawspaces-window_activatable.h 137 2006-04-23 15:13:27Z sfre $
 */

#ifndef __GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE_H__
#define __GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE_H__

#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS

#define GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE		(gedit_drawspaces_window_activatable_get_type ())
#define GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE(o)			(G_TYPE_CHECK_INSTANCE_CAST ((o), GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE, GeditDrawspacesWindowActivatable))
#define GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE_CLASS(k)		(G_TYPE_CHECK_CLASS_CAST((k), GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE, GeditDrawspacesWindowActivatableClass))
#define GEDIT_IS_DRAWSPACES_WINDOW_ACTIVATABLE(o)		(G_TYPE_CHECK_INSTANCE_TYPE ((o), GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE))
#define GEDIT_IS_DRAWSPACES_WINDOW_ACTIVATABLE_CLASS(k)		(G_TYPE_CHECK_CLASS_TYPE ((k), GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE))
#define GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE_GET_CLASS(o)	(G_TYPE_INSTANCE_GET_CLASS ((o), GEDIT_TYPE_DRAWSPACES_WINDOW_ACTIVATABLE, GeditDrawspacesWindowActivatableClass))

typedef struct _GeditDrawspacesWindowActivatable	GeditDrawspacesWindowActivatable;
typedef struct _GeditDrawspacesWindowActivatableClass	GeditDrawspacesWindowActivatableClass;

struct _GeditDrawspacesWindowActivatable
{
	GObject parent_instance;
};

struct _GeditDrawspacesWindowActivatableClass
{
	GObjectClass parent_class;
};

GType          gedit_drawspaces_window_activatable_get_type   (void) G_GNUC_CONST;

void           gedit_drawspaces_window_activatable_register   (GTypeModule *module);

G_END_DECLS

#endif /* __GEDIT_DRAWSPACES_WINDOW_ACTIVATABLE_H__ */
