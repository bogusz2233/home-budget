export class Formatter {
    static formatCurrency(value) {
        return new Intl.NumberFormat("pl-PL", {
            style: "currency",
            currency: "PLN",
        }).format(value);
    }

    static formatYearMonth(value) {
        return value || "—";
    }
}