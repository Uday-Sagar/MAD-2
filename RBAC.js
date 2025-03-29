const routes = [
    { path: "/", component: LandingPage },      
    { path: "/login", component: LoginPage },
    { path: "/signup", component: SignupPage },
    { path: "/unauthorized", component: UnauthorizedAccess },

    // ------------------- Admin paths -------------------
    { path: "/admin_home/:user_id", component: AdminHome, meta: { role: 'admin' } },

    // ------------------- Customer paths -------------------
    { path: "/customer_home/:user_id", component: CustomerHome, meta: { role: 'customer' } },
    { path: "/customer_profile/:user_id", component: CustomerProfile, meta: { role: 'customer' } },

    // ------------------- Service Professional paths -------------------
    { path: "/professional_home/:user_id", component: ProfessionalHome, meta: { role: 'service_professional' } },
    { path: "/professional_profile/:user_id", component: ProfessionalProfile, meta: { role: 'service_professional' } },
    { path: "/previous_services/:user_id", component: ProfessionalServices, meta: { role: 'service_professional' } },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// ------------------- Navigation Guard for Authentication -------------------
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');  // Check if user is logged in
    if (!token && to.path !== "/login" && to.path !== "/signup") {
        return next("/unauthorized"); // Redirect if user is not authenticated
    }

    // Decode JWT to get user role
    const user = JSON.parse(atob(token.split('.')[1])); // Decoding JWT payload
    const userRole = user.role;
    
    // Check if the route has a role restriction and user matches it
    if (to.meta.role && to.meta.role !== userRole) {
        return next("/unauthorized"); // Redirect unauthorized users
    }

    next(); // Allow access
});

export default router;
