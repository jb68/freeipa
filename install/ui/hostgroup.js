/*jsl:import ipa.js */

/*  Authors:
 *    Pavel Zuna <pzuna@redhat.com>
 *
 * Copyright (C) 2010 Red Hat
 * see file 'COPYING' for use and warranty information
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/* REQUIRES: ipa.js, details.js, search.js, add.js, entity.js */


IPA.entity_factories.hostgroup = function() {

    return IPA.entity_builder().
        entity('hostgroup').
        search_facet({columns:['cn','description'],
                      add_fields:['cn','description']}).
        details_facet({sections:[{
            name:'identity',
            label: IPA.messages.objects.hostgroup.identity,
            fields:['cn','description']
        }]}).
        association_facet({
            name: 'memberof_hostgroup',
            associator: IPA.serial_associator
        }).
        standard_association_facets().
        build();
};



