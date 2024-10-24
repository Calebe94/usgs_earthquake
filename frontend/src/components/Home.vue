<template>
  <div class="home-container">
    <h2>Select a City and Date Range for Earthquake Search</h2>
    <div class="form-container">
      <select v-model="selectedCity" class="city-dropdown">
        <option disabled value="">Select a city</option>
        <option v-for="city in cities" :key="city.id" :value="city.id">
          {{ city.name }}
        </option>
      </select>

      <input
        type="date"
        v-model="startDate"
        class="date-picker"
        placeholder="Start Date"
      />

      <input
        type="date"
        v-model="endDate"
        class="date-picker"
        placeholder="End Date"
      />

      <button @click="searchEarthquake" class="search-btn">
        Search Earthquakes
      </button>
      <button @click="createCity" class="create-city-btn">Create City</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- City Registration Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>Create City</h3>
        <form @submit.prevent="submitCity" class="modal-form">
          <div class="input-container">
            <label for="cityName">City Name:</label>
            <input type="text" id="cityName" v-model="newCity.name" required />
          </div>
          <div class="input-container">
            <label for="latitude">Latitude:</label>
            <input
              type="number"
              id="latitude"
              step="any"
              v-model.number="newCity.latitude"
            />
          </div>
          <div class="input-container">
            <label for="longitude">Longitude:</label>
            <input
              type="number"
              id="longitude"
              step="any"
              v-model.number="newCity.longitude"
            />
          </div>
          <button type="submit" class="submit-btn">Register City</button>
          <button type="button" @click="closeModal" class="cancel-btn">
            Cancel
          </button>
        </form>
        <div v-if="modalMessage" :class="['modal-message', modalMessageClass]">
          {{ modalMessage }}
        </div>
      </div>
    </div>

    <div v-if="earthquakeResults.length > 0" class="results-container">
      <h3>Earthquake Results</h3>
      <ul>
        <li v-for="result in earthquakeResults" :key="result.date">
          The closest Earthquake to {{ result.city }} was a M
          {{ result.magnitude }} - {{ result.place }} on
          {{ new Date(result.date).toLocaleString() }}
        </li>
      </ul>
    </div>

    <div v-if="history.length > 0" class="history-container">
      <h3>History of Results</h3>
      <table>
        <thead>
          <tr>
            <th>City</th>
            <th>Magnitude</th>
            <th>Place</th>
            <th>Date</th>
            <th>Distance (km)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in history" :key="result.date">
            <td>{{ result.city }}</td>
            <td>{{ result.magnitude }}</td>
            <td>{{ result.place }}</td>
            <td>{{ new Date(result.date).toLocaleString() }}</td>
            <td>{{ result.distance_km }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      cities: [],
      selectedCity: "",
      startDate: "",
      endDate: "",
      loading: false,
      errorMessage: "",
      earthquakeResults: [],
      showModal: false,
      newCity: {
        name: "",
        latitude: null,
        longitude: null,
      },
      modalMessage: "",
      history: [],
      modalMessageClass: "",
    };
  },
  mounted() {
    this.fetchCities();
    this.getHistory();
    document.title = "USGS Earthquake - Code Challenge";
  },
  methods: {
    fetchCities() {
      axios
        .get("/api/cities/")
        .then((response) => {
          this.cities = response.data;
        })
        .catch((error) => {
          console.error("Error fetching cities:", error);
          this.errorMessage = "Error loading cities.";
        });
    },
    closeModal() {
      this.showModal = false;
    },
    async submitCity() {
      this.modalMessageClass = "";
      try {
        const response = await axios.post("/api/cities/", this.newCity);
        this.cities.push(response.data);
        this.modalMessage = "City registered successfully!";
        this.closeModal();

        setTimeout(() => {
          this.modalMessageClass = "fade-out";
          setTimeout(() => {
            this.modalMessage = "";
            this.modalMessageClass = "";
          }, 500);
        }, 3000);
      } catch (error) {
        console.error("Error creating city:", error);
        this.modalMessage = "Error registering city.";
        this.modalMessageClass = "error";

        setTimeout(() => {
          this.modalMessageClass = "fade-out";
          setTimeout(() => {
            this.modalMessage = "";
            this.modalMessageClass = "";
          }, 500);
        }, 3000);
      }
    },

    createCity() {
      this.showModal = true;
      this.newCity = {
        name: "",
        latitude: null,
        longitude: null,
      };
      this.modalMessage = "";
    },
    async searchEarthquake() {
      if (!this.selectedCity || !this.startDate || !this.endDate) {
        this.errorMessage =
          "Please select a city and both start and end dates.";
        return;
      }

      this.loading = true;
      this.errorMessage = "";
      this.earthquakeResults = [];

      try {
        const response = await axios.get(
          `/api/cities/${this.selectedCity}/earthquakes/`,
          {
            params: { start_date: this.startDate, end_date: this.endDate },
          }
        );

        const requestId = response.data.id;
        console.log(
          "Request made for city:",
          this.selectedCity,
          " request id: ",
          requestId
        );

        await this.retryFetchResults(requestId);
      } catch (error) {
        console.error("Error searching earthquakes:", error);
        this.errorMessage = "Error fetching earthquake data.";
      } finally {
        this.loading = false;
      }
    },
    async getHistory() {
      try {
        const response = await axios.get(`/api/results/`);
        const results = response.data || [];

        const flattenedResults = results.flat().map((result) => {
          let date;
          try {
            date = new Date(result.date);
            if (isNaN(date.getTime())) {
              throw new Error("Invalid date");
            }
          } catch (error) {
            console.error("Error parsing date:", error);
            date = new Date();
          }

          return {
            city: result.city || "Unknown",
            date: date.toISOString(),
            place: result.place || "Unknown",
            magnitude: result.magnitude || 0,
            distance_km: result.distance_km || 0,
          };
        });

        this.history.push(...flattenedResults);
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    },
    async retryFetchResults(requestId) {
      let attempts = 0;
      const maxAttempts = 5;
      const delay = 500;

      while (attempts < maxAttempts) {
        try {
          const response = await axios.get(`/api/cities/results/${requestId}`);
          const results = response.data.result || [];

          console.log("Request result:", results, " request id: ", requestId);

          if (!Array.isArray(results) || results.length === 0) {
            attempts++;
            await this.delay(delay);
          } else {
            this.earthquakeResults = results;

            this.history.push(
              ...results.map((result) => ({
                ...result,
                date: new Date(result.date).toISOString(),
              }))
            );

            return;
          }
        } catch (error) {
          console.error("Error fetching results:", error);
        }

        attempts++;
        await this.delay(delay);
      }

      this.errorMessage =
        "Failed to fetch earthquake results after several attempts.";
    },
    delay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },
};
</script>
<style scoped>
.home-container {
  width: 50%;
  margin: 0 auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.city-dropdown,
.date-picker {
  padding: 10px;
  margin: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s;
}

.city-dropdown:focus,
.date-picker:focus {
  border-color: #007bff;
  outline: none;
}

.search-btn,
.create-city-btn {
  padding: 10px 20px;
  margin: 10px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-btn:hover,
.create-city-btn:hover {
  background-color: #0056b3;
}

.loading {
  color: #007bff;
  font-size: 18px;
  margin-top: 20px;
}

.error {
  color: red;
  margin-top: 20px;
}

.results-container {
  margin-top: 20px;
  text-align: left;
}

.history-container {
  margin-top: 40px;
  text-align: left;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

thead {
  background-color: #007bff;
  color: white;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tr:hover {
  background-color: #f1f1f1;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal h3 {
  margin-top: 0;
}

.modal-form {
  display: flex;
  flex-direction: column;
}

.input-container {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal input {
  width: 80%;
  margin-top: 5px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-btn,
.cancel-btn {
  padding: 10px 20px;
  margin-top: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn {
  background-color: #007bff;
  color: white;
}

.cancel-btn {
  background-color: #dc3545;
  color: white;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.cancel-btn:hover {
  background-color: #c82333;
}

.modal-message {
  margin-top: 15px;
  font-weight: bold;
}

.fade-out {
  opacity: 0;
  transition: opacity 0.5s ease-out;
}
</style>
