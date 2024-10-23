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

    <div v-if="earthquakeResults.length > 0" class="results-container">
      <h3>Earthquake Results</h3>
      <ul>
        <li v-for="result in earthquakeResults" :key="result.date">
          {{ result.place }} - Magnitude: {{ result.magnitude }} (Distance:
          {{ result.distance_km }} km)
        </li>
      </ul>
    </div>

    <div v-if="history" class="history-container">
      <h3>History of Results</h3>
      <table></table>
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
    };
  },
  mounted() {
    this.fetchCities();
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
    createCity() {
      alert("Create City functionality not implemented yet.");
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
</style>
