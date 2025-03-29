<template>
    <div class="cust-layout">
        <CustomerNavBar />
        <div class="cust-main-content">
            <h3><strong>Rate Your Service</strong></h3>

            <div v-if="loading" class="loading">Loading service details...</div>
            <div v-if="errorMessage" class="error"><strong>{{ errorMessage }}</strong></div>
            <div v-else class="rating-form">
                <p><strong>Service: </strong><strong>{{ service.serviceType }}</strong></p>
                <p><strong>Professional: </strong><strong>{{ service.professionalName }}</strong></p>

                <div class="rating-section">
                    <label><strong>Rating (1-5):</strong></label>
                    <div class="stars">
                        <span v-for="star in 5" :key="star" 
                              @click="rating = star" 
                              :class="{ 'selected': star <= rating }">
                            ★
                        </span>
                    </div>
                </div>

                <div class="comment-section">
                    <label><strong>Additional Comments:</strong></label>
                    <textarea v-model="comment" placeholder="Write your feedback..."></textarea>
                </div>

                <button @click="submitRating" class="submit-btn">Submit Rating</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
  name: 'SubmitRatings',
  components: { CustomerNavBar },
  data() {
    return {
      userId: this.$route.params.user_id,
      serviceId: this.$route.params.service_id,
      service: {},
      rating: 0,
      comment: '',
      loading: true,
      errorMessage: '',
    };
  },
  mounted() {
    console.log("Service ID:", this.serviceId);
    this.fetchServiceDetails();
  },
  methods: {
    async fetchServiceDetails() {
        console.log(`Fetching: http://127.0.0.1:7644/get_service_details/${this.serviceId}`);
        try {
            const response = await axios.get(`http://127.0.0.1:7644/get_service_details/${this.serviceId}`);
            console.log("Response:", response.data);
            if (response.data.success) {
            this.service = response.data.service;
            } else {
            this.errorMessage = response.data.message;
            }
        } catch (error) {
            console.error("Error fetching service details:", error);
            this.errorMessage = "Error fetching service details.";
        } finally {
            this.loading = false;
        }
        },
    async submitRating() {
        if (this.rating < 1 || this.rating > 5) {
            alert("Please select a rating between 1 and 5.");
            return;
        }

        try {
            const response = await axios.post(`http://127.0.0.1:7644/submit_service_rating`, {
            user_id: parseInt(this.userId), // Ensure it's an integer
            service_id: parseInt(this.serviceId), // Ensure it's an integer
            rating: this.rating,
            comment: this.comment
            });

            if (response.data.success) {
            alert("Thank you for your feedback!");
            this.$router.push(`/customer_home/${this.userId}`);
            } else {
            alert(response.data.message || "Failed to submit rating. Please try again.");
            }
        } catch (error) {
            alert("Error submitting rating. Please try again later.");
        }
    }
  }
};
</script>

<style scoped>
/* Layout */
.rating-form {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: auto;
}

.rating-section, .comment-section {
  margin-bottom: 15px;
}

/* Star Rating */
.stars {
  display: flex;
  font-size: 24px;
  cursor: pointer;
  color: gray;
}

.stars span {
  margin-right: 5px;
}

.stars span.selected {
  color: gold;
}

/* Comment Box */
textarea {
  width: 100%;
  height: 80px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Submit Button */
.submit-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #218838;
}

/* Loading & Error */
.loading, .error {
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
}

.error {
  color: red;
}
</style>
