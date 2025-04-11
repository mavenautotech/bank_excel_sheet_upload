odoo.define('vehicle.list_view_button', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc');

    var TreeButton = ListController.extend({
        buttons_template: 'vehicle.buttons',

        events: _.extend({}, ListController.prototype.events, {
            'click .btn.btn-primary.ms-2': '_onScanButtonClick',
        }),

        _onScanButtonClick: function (ev) {
            ev.preventDefault();

            // Use static ID (1)
            rpc.query({
                model: 'vehicle.data',
                method: 'action_get_file_from_ftp',
                args: [1], // Pass static ID
            }).then(function (result) {
                if (result && result.url) {
                    window.open(result.url, '_blank');
                }

                // Reload the page after fetching the files
                location.reload();
            }).catch(function (error) {
                console.error('Error while calling action_scan:', error);
            });
        },
    });

    var PickingListView = ListView.extend({
        config: Object.assign({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });

    viewRegistry.add('button_in_vehicle_tree', PickingListView);
});
