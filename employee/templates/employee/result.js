let ResultViewModel = {
    data: {},
    models: {
        results: ko.observableArray([]),
    },
    methods: {},
    services: {
        all: function () {
            axios.get("{% url 'employee:ajax-result-list' %}").then(function (response) {
                ResultViewModel.models.results(response.data);
            })
        }
    }
};

ko.computed(function () {
    ResultViewModel.services.all();
});

ko.applyBindings([ResultViewModel]);