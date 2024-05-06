if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    change_draggable_zone: function() {
        console.log("Initializing make_draggable function");
        return new Promise((resolve, reject) => {
            try {
                // Assuming that each route container has a class 'route-draggable-area'
                let routeContainers = document.querySelectorAll('.route-draggable-area');

                // Initialize dragula for each route container
                let drake = dragula(Array.from(routeContainers));

                drake.on('drop', function(el, target, source, sibling) {
                    // Construct the new order data for each route container
                    let newOrder = {};
                    routeContainers.forEach(function(container) {
                        let routeId = container.id;  // Using the container's ID as the route ID
                        let requestIds = Array.from(container.querySelectorAll('.draggable-card')).map(function(card) {
                            return card.id;  // Assuming each card has a unique ID
                        });
                        newOrder[routeId] = requestIds; // Log new order
                    });

                    console.log("Final newOrder object:", newOrder);
                    resolve(JSON.stringify(newOrder)); // Resolve the promise with the new order
                });

                console.log("make_draggable setup complete");
            } catch (error) {
                console.error("Error in make_draggable:", error);
                reject(error); // Indicate failure
            }
        });
    }
}
