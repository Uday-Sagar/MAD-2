<template>
    <div class="bg-light">
        <nav class="navbar">
            <div class="logo">
            <img src="/logo.png" alt="Logo" />
            <h1><strong>HomiCare</strong></h1>
            </div>
            <div class="buttons">
                <button type="button" class="btn btn-primary" @click="navigateToSignUp">Signup</button>
                <button type="button" class="btn btn-primary" @click="navigateToLogin">Login</button>
            </div>
        </nav>
        <div class="cream-violet-band">
            <span class="mx-auto lead">Book trusted professionals for AC repair, furniture repair, plumbing, and more.</span>
        </div>

        <div class="container py-5">
            <h2 class="text-center mb-4">Our Services</h2>
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm">
                        <img src="/images/ac-repair.jpg" class="card-img-top" alt="AC Repair">
                        <div class="card-body">
                            <h5 class="card-title"><strong>AC Repair</strong></h5>
                            <p class="card-text">Expert AC repair services to keep you cool during summer.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm">
                        <img src="/images/furniture-repair.jpg" class="card-img-top" alt="Furniture Repair">
                        <div class="card-body">
                            <h5 class="card-title"><strong>Furniture Repair</strong></h5>
                            <p class="card-text">Skilled professionals to restore your furniture to perfection.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm">
                        <img src="/images/plumbing.jpg" class="card-img-top" alt="Plumbing">
                        <div class="card-body">
                            <h5 class="card-title"><strong>Plumbing</strong></h5>
                            <p class="card-text">Quick and reliable plumbing solutions for your home.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LandingPage",
    methods: {
        navigateToSignUp() {
            this.$router.push('/signup');
        },
        navigateToLogin() {
            this.$router.push('/login');
        }
    }
};
</script>

<style>
.card img {
    height: 200px;
    object-fit: cover;
}
</style>
