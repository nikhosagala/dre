let EmployeeViewModel = {
    data: {},
    models: {
        employees: ko.observableArray([]),
    },
    methods: {},
    services: {
        all: function () {
            axios.get("{% url 'employee:ajax-employee-list' %}").then(function (response) {
                EmployeeViewModel.models.employees(response.data);
            })
        }
    }
};

ko.computed(function () {
    EmployeeViewModel.services.all();
});

ko.applyBindings([EmployeeViewModel]);