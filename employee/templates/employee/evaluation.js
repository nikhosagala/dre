let EmployeeViewModel = {
    data: {},
    models: {
        questions: ko.observableArray([])
    },
    methods: {
        onClickButtonSubmit: (data, event) => {
        }
    },
    services: {
        get: () => {
            axios.get("{{ evaluation_url }}").then(
                (response) => EmployeeViewModel.models.questions(response)
            )
        },
    }
};

ko.computed(() => EmployeeViewModel.services.get());

ko.applyBindings([EmployeeViewModel]);