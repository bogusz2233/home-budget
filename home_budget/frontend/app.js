import { Defines } from "./defines.js";
import { Formatter } from "./formatter.js";

const elements = {
    filtersForm: document.getElementById("filtersForm"),
    createForm: document.getElementById("createForm"),
    propertiesTable: document.getElementById("propertiesTable"),
    emptyState: document.getElementById("emptyState"),
    totalValue: document.getElementById("totalValue"),
    totalCount: document.getElementById("totalCount"),
    quickSearch: document.getElementById("quickSearch"),
    refresh: document.getElementById("refresh"),
    clearFilters: document.getElementById("clearFilters"),
    createNotice: document.getElementById("createNotice"),
    typeFilter: document.getElementById("typeFilter"),
    typeCreate: document.getElementById("typeCreate"),
    creationMonthFilter: document.getElementById("creation_month"),
    creationYearFilter: document.getElementById("creation_year"),
};

const normalizeFilterValue = (key, value) => {
    if (!value) {
        return null;
    }

    if (key === "creation_year" || key === "creation_month") {
        const numeric = Number(value);
        if (Number.isNaN(numeric)) {
            return null;
        }
        return String(numeric);
    }

    if (key === "type") {
        return value.toLowerCase();
    }

    return value;
};

const buildTypeOption = (type) => {
    const option = document.createElement("option");
    option.value = type;
    option.textContent = Defines.PROPERTY_TYPES[type] || type;
    return option;
};

const buildSelectOptions = () => {
    Object.keys(Defines.PROPERTY_TYPES).forEach((type) => {
        const option = buildTypeOption(type);
        elements.typeCreate.appendChild(option);
        elements.typeFilter.appendChild(option.cloneNode(true));
    });
};

const getFilters = () => {
    const data = new FormData(elements.filtersForm);
    const params = new URLSearchParams();

    for (const [key, value] of data.entries()) {
        const normalized = normalizeFilterValue(key, value);
        if (normalized !== null) {
            params.append(key, normalized);
        }
    }

    const quick = elements.quickSearch.value.trim();
    if (quick) {
        params.set("name", quick);
    }

    return params;
};

const renderTable = (items) => {
    elements.propertiesTable.innerHTML = "";

    const header = document.createElement("div");
    header.className = "table-header";
    header.innerHTML =
        "<div>Name</div><div>Type</div><div>Amount</div><div>Created</div><div>Actions</div>";
    elements.propertiesTable.appendChild(header);

    items.forEach((item) => {
        const row = document.createElement("div");
        row.className = "table-row";
        row.innerHTML = createRowTemplate(item);
        elements.propertiesTable.appendChild(row);
    });

    elements.emptyState.style.display = items.length ? "none" : "block";
};

const createRowTemplate = (item) => `
      <div>${item.name}</div>
      <div>${Defines.PROPERTY_TYPES[item.type.toUpperCase()] || item.type}</div>
      <div>${Formatter.formatCurrency(item.amount)}</div>
      <div>${Formatter.formatDate(item.creation_time)}</div>
            <div>
                <button class="danger icon-button" type="button" data-action="delete" data-id="${item.id_p}" aria-label="Delete">🗑️</button>
            </div>
    `;

const updateStats = (items) => {
    const total = items.reduce((sum, item) => sum + Number(item.amount || 0), 0);
    elements.totalValue.textContent = Formatter.formatCurrency(total);
    elements.totalCount.textContent = items.length;
};

const loadProperties = async () => {
    const params = getFilters();
    const url = params.toString() ? `/api/properties?${params}` : "/api/properties";

    const response = await fetch(url);
    if (!response.ok) {
        throw new Error("Failed to load properties");
    }

    const data = await response.json();
    renderTable(data);
    updateStats(data);
};

const handleCreate = async (event) => {
    event.preventDefault();
    elements.createNotice.textContent = "";

    const data = new FormData(elements.createForm);
    const payload = Object.fromEntries(data.entries());
    payload.type = payload.type.toLowerCase();
    payload.amount = Number(payload.amount);
    payload.creation_time = new Date(payload.creation_time).toISOString();

    const response = await fetch("/api/properties", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const error = await response.text();
        elements.createNotice.textContent = `Could not save: ${error}`;
        return;
    }

    elements.createNotice.textContent = "Property saved.";
    elements.createForm.reset();
    await loadProperties();
};

const handleDelete = async (propertyId) => {
    elements.createNotice.textContent = "";

    const response = await fetch(`/api/properties/${propertyId}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        const error = await response.text();
        elements.createNotice.textContent = `Could not delete: ${error}`;
        return;
    }

    await loadProperties();
};

const handleTableClick = async (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
        return;
    }

    if (target.dataset.action !== "delete") {
        return;
    }

    const propertyId = Number(target.dataset.id);
    if (Number.isNaN(propertyId)) {
        return;
    }

    await handleDelete(propertyId);
};

const handleFilterSubmit = async (event) => {
    event.preventDefault();
    await loadProperties();
};

const clearFilters = async () => {
    elements.filtersForm.reset();
    elements.quickSearch.value = "";
    await loadProperties();
};

const debounce = (callback, delay) => {
    let timerId;
    return (...args) => {
        if (timerId) {
            clearTimeout(timerId);
        }
        timerId = setTimeout(() => callback(...args), delay);
    };
};




const bootstrap = async () => {
    buildSelectOptions();
    elements.createForm.addEventListener("submit", handleCreate);
    elements.filtersForm.addEventListener("submit", handleFilterSubmit);
    elements.refresh.addEventListener("click", loadProperties);
    elements.clearFilters.addEventListener("click", clearFilters);
    elements.quickSearch.addEventListener("input", debounce(loadProperties, 250));
    elements.propertiesTable.addEventListener("click", handleTableClick);

    await loadProperties();
};

bootstrap().catch((error) => {
    elements.createNotice.textContent = error.message;
});
