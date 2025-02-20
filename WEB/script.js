document.addEventListener("DOMContentLoaded", () => {
    const toggleModeBtn = document.getElementById("toggleMode");
    const autoModeDiv = document.getElementById("autoMode");
    const manualModeDiv = document.getElementById("manualMode");
    const refreshDataBtn = document.getElementById("refreshData");
    const ecowattDataDiv = document.getElementById("ecowattData");
    const relayButtons = document.querySelectorAll(".relay-btn");
    const checkboxes = document.querySelectorAll(".hvalue-checkbox");

    let currentMode = "auto";

    async function fetchCurrentMode() {
        try {
            const response = await fetch("http://127.0.0.1:8000/mode");
            if (!response.ok) throw new Error("Erreur lors de la récupération de l'état du mode");
            const data = await response.json();
            currentMode = data.mode || "auto";
            updateModeDisplay();
        } catch (error) {
            console.error("Erreur lors de la récupération du mode :", error);
        }
    }

    function updateModeDisplay() {
        if (currentMode === "auto") {
            autoModeDiv.style.display = "block";
            manualModeDiv.style.display = "none";
        } else {
            autoModeDiv.style.display = "none";
            manualModeDiv.style.display = "block";
        }
        toggleModeBtn.textContent = `Passer au mode ${currentMode === "auto" ? "manuel" : "automatique"}`;
    }

    async function toggleMode() {
        const newMode = currentMode === "auto" ? "manual" : "auto";
        try {
            await fetch("http://127.0.0.1:8000/mode", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mode: newMode })
            });
            currentMode = newMode;
            updateModeDisplay();
        } catch (error) {
            console.error("Erreur lors du changement de mode:", error);
        }
    }

    toggleModeBtn.addEventListener("click", toggleMode);

    async function fetchRelayStates() {
        try {
            const response = await fetch("http://127.0.0.1:8000/get_relays_state");
            if (!response.ok) throw new Error("Erreur lors de la récupération des états");
            const data = await response.json();
            relayButtons.forEach(checkbox => {
                const relayId = parseInt(checkbox.dataset.relay);
                checkbox.checked = data[relayId] || false;
            });
        } catch (error) {
            console.error("Erreur lors de la récupération des états :", error);
        }
    }

    relayButtons.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            const relayId = parseInt(this.dataset.relay);
            fetch("http://127.0.0.1:8000/phidget", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ relay: relayId, state: this.checked })
            })
            .then(response => {
                if (!response.ok) throw new Error('Erreur HTTP : ' + response.status);
                return response.json();
            })
            .catch(error => {
                console.error("Erreur lors de la requête :", error);
                alert("Erreur de connexion au serveur !");
                this.checked = !this.checked;
            });
        });
    });

    // Ajout des événements pour les checkboxes

    function attachHvalueCheckboxListeners() {
        const checkboxes = document.querySelectorAll(".hvalue-checkbox");

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener("change", async (e) => {
                const signal = e.target.dataset.signal;
                const pas = e.target.dataset.value;
                const newState = e.target.checked ? 1 : 0;

                try {
                    const response = await fetch("http://127.0.0.1:8000/update_hvalue", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            signal: signal,
                            pas: pas,
                            hvalue: newState
                        })
                    });

                    if (!response.ok) {
                        throw new Error("Erreur lors de la mise à jour de hvalue");
                    }

                    console.log(`hvalue mis à jour: signal=${signal}, pas=${pas}, hvalue=${newState}`);
                } catch (error) {
                    console.error("Erreur lors de la mise à jour de hvalue:", error);
                }
            });
        });
    }

    async function fetchEcowattData() {
        try {
            const response = await fetch("http://127.0.0.1:8000/ecowatt");
            if (!response.ok) {
                throw new Error("Erreur lors de la récupération des données EcoWatt");
            }
            const data = await response.json();
            const signals = data.data.signals;

            // Création du tableau des données
            const tableBody = document.querySelector("#ecowattTable tbody");
            tableBody.innerHTML = ""; // Clear previous data

            signals.forEach(signal => {
                signal.values.forEach(value => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${signal.GenerationFichier}</td>
                        <td>${signal.jour}</td>
                        <td>${signal.message}</td>
                        <td>${signal.dvalue}</td>
                        <td>${value.pas}</td>
                        <td><input type="checkbox" class="hvalue-checkbox" data-signal="${signal.jour}" data-value="${value.pas}" ${value.hvalue === 1 ? "checked" : ""}></td>
                    `;
                    tableBody.appendChild(row);
                });
            });

            // Réattache les écouteurs après mise à jour du DOM
            attachHvalueCheckboxListeners();
        } catch (error) {
            console.error("Erreur lors de la récupération des données EcoWatt:", error);
        }

    }

    refreshDataBtn.addEventListener("click", async () => {
        try {
            await fetch("http://127.0.0.1:8000/refresh", { method: "POST" });
            fetchEcowattData();
        } catch (error) {
            console.error("Erreur lors du rafraîchissement des données:", error);
        }
        fetchRelayStates
    });

    // Fonction pour contrôler le relais
    async function controlRelay(state) {
        try {
            const relayState = state ? "allumer" : "éteindre";
            await fetch("http://127.0.0.1:8000/phidget", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ relay: 1, state })
            });
            console.log(`Relais 1 ${relayState}`);
        } catch (error) {
            console.error("Erreur lors du contrôle du relais:", error);
        }
    }

    fetchEcowattData();
    fetchCurrentMode();
    fetchRelayStates();
    setInterval(fetchEcowattData, 10000);
});
