<script>
  import { goto } from '$app/navigation';

  let username = '';
  let password = '';
  let errorMsg = '';

  async function handleSignup() {
    try {
      // First, call the signup endpoint
      const signupResponse = await fetch('http://localhost:8000/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!signupResponse.ok) {
        const errData = await signupResponse.json();
        errorMsg = typeof errData.detail === 'string'
          ? errData.detail
          : JSON.stringify(errData.detail);
        return;
      }
      
      // If signup is successful, automatically log in the user.
      const loginResponse = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!loginResponse.ok) {
        const errData = await loginResponse.json();
        errorMsg = typeof errData.detail === 'string'
          ? errData.detail
          : JSON.stringify(errData.detail);
        return;
      }
      const data = await loginResponse.json();

      // Store user info in localStorage
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('username', data.username);
      // Optionally store the access token if provided by the login endpoint
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }

      // Redirect to home page
      goto('/');
    } catch (error) {
      errorMsg = 'Network error during signup.';
      console.error(error);
    }
  }

  function goToLogin() {
    goto('/login');
  }
</script>

<style>
  .container {
    max-width: 400px;
    margin: 5rem auto;
    padding: 2rem;
    background-color: #ffffff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
  }

  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }

  /* Primary signup button */
  .signup-btn {
    background-color: #4f46e5;
    color: #fff;
    margin-bottom: 1rem;
  }
  .signup-btn:hover {
    background-color: #4338ca;
  }

  /* Secondary button to go back to login */
  .login-btn {
    background-color: #fff;
    color: #4f46e5;
    border: 2px solid #4f46e5;
    margin-top: 0.5rem;
  }
  .login-btn:hover {
    background-color: #4f46e5;
    color: #fff;
  }

  .error {
    color: #dc2626;
    margin-top: 0.5rem;
    text-align: center;
  }
</style>

<div class="container">
  <h1>Sign Up</h1>
  <div>
    <label for="username">Username</label>
    <input
      id="username"
      type="text"
      bind:value={username}
      placeholder="Enter your username"
    />
  </div>
  <div>
    <label for="password">Password</label>
    <input
      id="password"
      type="password"
      bind:value={password}
      placeholder="Enter your password"
    />
  </div>

  <button class="signup-btn" on:click={handleSignup}>Sign Up</button>
  <button class="login-btn" on:click={goToLogin}>Back to Login</button>

  {#if errorMsg}
    <div class="error">{errorMsg}</div>
  {/if}
</div>
