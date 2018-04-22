let EmployeeViewModel = {
    data: {},
    models: {
        questions: ko.observableArray([]),
        answers: ko.observableArray([]),
        values: ko.observableArray([]),
    },
    methods: {
        onClickButtonSubmit: (data, event) => {
            EmployeeViewModel.models.values().forEach((value, index) => {
                EmployeeViewModel.models.answers()[index].value = value;
            });
            let submit = {
                period: $('#period').val(),
                answers: EmployeeViewModel.models.answers(),
            };
            EmployeeViewModel.services.add(submit);
        }
    },
    services: {
        get: () => {
            axios.get("{{ promotion_url }}").then(
                (response) => EmployeeViewModel.models.questions(response.data)
            ).then(() => {
                EmployeeViewModel.models.questions().forEach((value) => {
                    let answer = {
                        question: value,
                        value: 0
                    };
                    EmployeeViewModel.models.answers.push(answer);
                })
            });
        },
        add: (data) => {
            axios.post("{{ promotion_url}}", ko.toJSON(data)).then(() => window.location.href = "{% url 'employee:result' %}");
        }
    }
};

ko.computed(() => EmployeeViewModel.services.get());

ko.applyBindings([EmployeeViewModel]);