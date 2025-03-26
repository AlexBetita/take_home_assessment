<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let userId;
  let userName;
  // Use an object to hold dynamic totals for items
  let totals = {};
  let orders = [];
  let driveThruMessage = '';
  let driveThruError = '';
  let commandResponse = ''; // To display the bot response

  onMount(async () => {
    // Check if the user is logged in
    userId = localStorage.getItem('user_id');
    userName = localStorage.getItem('username');

    if (!userId || !userName) {
      goto('/login');
      return;
    }
    await fetchData();
  });

  // Function to fetch totals and order history
  async function fetchData() {
    try {
      const itemsRes = await fetch('http://localhost:8000/api/order_items');
      const itemsData = await itemsRes.json();
      totals = {};
      for (const row of itemsData) {
        const name = row.item_name;
        totals[name] = totals[name] ? totals[name] + row.total_quantity : row.total_quantity;
      }
      const ordersRes = await fetch('http://localhost:8000/api/orders');
      orders = await ordersRes.json();
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Function to send drive-thru messages and update page accordingly
  async function sendMessage() {
    try {
      const res = await fetch('http://localhost:8000/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: driveThruMessage, user_id: parseInt(userId) })
      });

      if (!res.ok) {
        const errData = await res.json();
        driveThruError = errData.detail || 'Error sending command';
        return;
      } else {
        driveThruError = '';
      }

      const data = await res.json();
      // Save the bot response text
      commandResponse = data.bot_response || '';

      // If an order was created or deleted, refresh totals and order history
      if (data.response && (data.response.order_number || data.response.status)) {
        await fetchData();
      }
    } catch (error) {
      driveThruError = 'Network error sending command';
      console.error('Error sending message:', error);
    }
  }

  function logout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('access_token');
    goto('/login');
  }
</script>

<style>
  .container {
    width: 100%;
    min-height: 100vh;
    padding: 2rem;
    background-color: #ffffff;
  }

  .welcome {
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
    font-weight: 500;
  }

  .logout {
    text-align: right;
    margin-bottom: 1.5rem;
  }

  .logout button {
    background-color: #fff;
    color: #4f46e5;
    border: 2px solid #4f46e5;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }

  .logout button:hover {
    background-color: #4f46e5;
    color: #fff;
  }

  /* Totals styling; flex-wrap allows for a dynamic number of items */
  .totals {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    margin-bottom: 1.5rem;
  }
  .totalBox {
    flex: 1 1 30%;
    margin: 0.5rem;
    background-color: #f9f9f9;
    border-radius: 4px;
    text-align: center;
    padding: 1rem;
  }

  .driveThru {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .driveThru input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  .driveThru button {
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 4px;
    background-color: #4f46e5;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }
  .driveThru button:hover {
    background-color: #4338ca;
  }

  .error {
    color: #dc2626;
    text-align: center;
    margin-bottom: 1rem;
  }

  /* Styling for the command response message */
  .commandResponse {
    background: #f0f4ff;
    border: 1px solid #4f46e5;
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1rem;
    color: #4f46e5;
  }

  .orderHistory {
    margin-top: 2rem;
  }
  .orderHistory h2 {
    text-align: center;
    margin-bottom: 1rem;
  }
  .orderHistory ul {
    list-style: none;
    padding: 0;
  }
  .orderHistory li {
    background: #fafafa;
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 4px;
  }
  .orderHistory li strong {
    display: block;
    margin-bottom: 0.5rem;
  }
</style>

<div class="container">
  <!-- Logout Button -->
  <div class="logout">
    <button on:click={logout}>Logout</button>
  </div>

  <!-- Welcome Message -->
  <div class="welcome">
    Welcome, {userName}!
  </div>

  <!-- Totals Section (dynamic items) -->
  <div class="totals">
    {#each Object.entries(totals) as [itemName, total]}
      <div class="totalBox">
        <h3>{itemName}</h3>
        <p>{total}</p>
      </div>
    {/each}
  </div>

  <!-- Drive Thru Message -->
  <div class="driveThru">
    <input
      type="text"
      placeholder="Drive thru message (e.g., 'I want one burger, one fry')"
      bind:value={driveThruMessage}
    />
    <button on:click={sendMessage}>Run</button>
  </div>
  
  {#if driveThruError}
    <div class="error">{driveThruError}</div>
  {/if}

  <!-- Display Bot Response -->
  {#if commandResponse}
    <div class="commandResponse">{commandResponse}</div>
  {/if}

  <!-- Order History -->
  <div class="orderHistory">
    <h2>Order History</h2>
    <ul>
      {#each orders as order}
        <li>
          <strong>Order #{order.order_number}</strong> (User ID: {order.user_id})
          {#each order.items as item}
            <div>{item.quantity} × {item.item_name}</div>
          {/each}
        </li>
      {/each}
    </ul>
  </div>
</div>
