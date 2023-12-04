//** @odoo-module */
const { Component, onMounted, useState, onWillStart } = owl;
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { Domain } from "@web/core/domain";
import rpc from 'web.rpc';

class CustomListController extends ListController {
    setup() {
        super.setup(...arguments);
        this.loadSalesperson = useState({ data: null });
        this.selectedSalesperson = useState({ id: null, name: null });
        this.orm = useService("orm");

        onWillStart(async() => {
            await this.loadData();
        });
    }
    async loadData() {
        try {
            const data = await this.orm.call(
            'res.users',
            'search_read',
            [[['share', '=', false]]],
            )
            this.loadSalesperson.data = data;
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    async updateFilter() {
        try {
            const domain = [['user_id', 'like', this.selectedSalesperson.id]];
            let preFilters = {
                description: `Salesperson is "${this.selectedSalesperson.name}"`,
                domain: new Domain(domain).toString(),
                type: "filter",
            };
            // Check if createNewFilters method is available on this.env.searchModel
            if (this.env.searchModel.createNewFilters) {
                // Use the createNewFilters method with the updated domain
                this.env.searchModel.createNewFilters([preFilters]);
            } else {
                console.error('Error: createNewFilters method is not available on this.env.searchModel.');
            }
        } catch (error) {
            console.error('Error updating filter:', error);
        }
    }

    applyPreFilter() {
        // Clear existing filters
        this.clearFilters();

        const preFilters = [{
            description: `Salesperson is "${this.selectedSalesperson.name}"`,
            domain: [['user_id', '=', this.selectedSalesperson.id]],
        }];
        // Call createNewFilters from this.env.searchModel
        if (this.env.searchModel.createNewFilters) {
            this.env.searchModel.createNewFilters(preFilters[0].domain); // Pass only the domain
            // Notify the UI about the changes
            this._notify();
        } else {
            console.error('Error: createNewFilters method is not available on this.env.searchModel.');
        }
    }

    onUserChange(ev) {
        const selectedOption = ev.target.options[ev.target.selectedIndex];
        const userId = selectedOption.value;
        const userName = selectedOption.text;

        this.selectedSalesperson = { id: userId, name: userName };
        this.updateFilter();
    }

    // Clear existing filters
    clearFilters() {
        // Check if this.env.searchModel is defined
        if (!this.env.searchModel) {
            console.error('Error: this.env.searchModel is not defined.');
            return;
        }

        // Clear filters in SearchModel
        this.env.searchModel.query = [];
        this.env.searchModel.searchItems = {};
        this.nextGroupId++;
        this.nextGroupNumber++;
        this.nextId++;

        this._notify();
    }
}

CustomListController.template = "salesperson_dropdown_crm.listView";

export const customListView = {
    ...listView,
    Controller: CustomListController,
};

registry.category("views").add("salesperson_dropdown", customListView);
