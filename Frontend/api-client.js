(function () {
  'use strict';

  const apiBaseUrl = 'http://localhost:8000';

  async function request(path, options = {}) {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      let detail = `${response.status} ${response.statusText}`;
      try {
        const payload = await response.json();
        detail = payload.detail || payload.message || detail;
      } catch (error) {
        // Fall back to the status text when the body is not JSON.
      }
      throw new Error(detail);
    }

    return response.json();
  }

  async function resolveDemoUser() {
    const users = await request('/users');
    const demoUser = users.find((user) => user.email === 'alex@demo.com');
    if (demoUser) {
      return demoUser;
    }

    if (users.length > 0) {
      return users[0];
    }

    return request('/user', {
      method: 'POST',
      body: JSON.stringify({ name: 'Alex Chen', email: 'alex@demo.com' }),
    });
  }

  window.FutureFlexAPI = {
    baseUrl: apiBaseUrl,
    request,
    health: () => request('/'),
    getUsers: () => request('/users'),
    createUser: (payload) => request('/user', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
    getUser: (userId) => request(`/user/${userId}`),
    getDashboard: (userId) => request(`/dashboard/${userId}`),
    getXpSummary: (userId) => request(`/xp/${userId}`),
    getRewards: (userId) => request(`/rewards/${userId}`),
    getHabitsToday: (userId) => request(`/habits/today/${userId}`),
    getRoundups: (userId) => request(`/roundups/${userId}`),
    getKycStatus: (userId) => request(`/onboard/kyc-status/${userId}`),
    resolveDemoUser,
    getGoal: (userId) => request(`/goals/${userId}`),
    getGoals: (userId) => request(`/goals/${userId}/all`),
    updateGoal: (userId, payload) => request(`/goals/${userId}`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
    setGoal: (payload) => request(`/goals/${payload.user_id}`, {
      method: 'POST',
      body: JSON.stringify({
        goal: payload.goal,
        target_amount: payload.target_amount,
      }),
    }),
    // Onboarding deposits
    makeDeposit: (userId, amount) => request('/onboard/deposit', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, amount: amount }),
    }),
  };
})();