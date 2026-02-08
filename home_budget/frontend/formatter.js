export class Formatter {
    static formatCurrency(value) {
        return new Intl.NumberFormat("pl-PL", {
            style: "currency",
            currency: "PLN",
        }).format(value);
    }

    static formatDate(value) {
        return new Intl.DateTimeFormat("pl-PL", {
            dateStyle: "medium",
            timeStyle: "short",
        }).format(new Date(value));
    }
}