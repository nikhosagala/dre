var EmployeeViewModel = {
    data: {},
    models: {
        message: ko.observable(null),
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
    EmployeeViewModel.models.message('Heloooo');
    EmployeeViewModel.services.all();
});

ko.applyBindings([EmployeeViewModel]);