<script setup>
  import { ref } from "vue";
  import { getTopHighlights } from "./service/highlights";

  const loadingInProgress = ref(false);
  const useOwnCredentials = ref(true);
  const username = ref("");
  const password = ref("");
  const email = ref("");

  const highlights = ref([]);
  const newData = ref({});

  const error = ref(false);
  const errorMessage = ref("");

  const radios = [
    {
      name: "Use my own credentials",
      description: "Using your credentials prevents request limitations and ensures uninterrupted scraping. Rest assured, your details are not stored or shared.",
      value: "yes",
      checked: true,
    },
    {
      name: "No, I don't want to use my own credentials",
      description: "Opting out may lead to request blocks due to service limitations, potentially impacting scraping reliability.",
      value: "no",
      checked: false,
    },
  ];

  const handleRadioClick = (value) => {
    if (value == "yes") {
      useOwnCredentials.value = true;
      radios[0].checked = true;
      radios[1].checked = false;
    } else {
      useOwnCredentials.value = false;
      radios[0].checked = false;
      radios[1].checked = true;
    }
  };

  async function handleFetchHighlightsClick() {
    loadingInProgress.value = true;
    error.value = false;
    errorMessage.value = "";
    const data = {};
    highlights.value = [];
    newData.value = {};
    if (!useOwnCredentials.value) {
      username.value = "";
      password.value = "";
      email.value = "";
    }
    if (
      username.value != null &&
      username.value != undefined &&
      username.value.length > 0
    ) {
      data.username = username.value;
    }
    if (
      email.value != null &&
      email.value != undefined &&
      email.value.length > 0
    ) {
      data.email = email.value;
    }
    if (
      password.value != null &&
      password.value != undefined &&
      password.value.length > 0
    ) {
      data.username = password.value;
    }

    const result = await getTopHighlights(data);
    if (result.code == 1){
      console.log(result.data)
      newData.value = result.data;
      highlights.value = result.data.topics
    }
    else {
      error.value = true;
      errorMessage.value = result.message;
    }
    loadingInProgress.value = false;
  }
</script>

<template>
  <body
    class="w-[100dvw] bg-[#060606] text-white px-3 py-2 items-center justify-center min-h-[100dvh] overflow-x-hidden flex flex-col gap-y-2"
  >
    <div
      class="flex flex-col gap-y-2 justify-center items-center max-w-[600px]"
    >
      <h2 class="font-medium text-[calc(16px+0.2dvw)] tracking-wide">
        Select Credentials type
      </h2>
      <ul class="gap-x-4 flex-wrap gap-y-3 flex justify-center">
        <li v-for="(item, idx) in radios" :key="idx">
          <label :for="item.name" class="block relative">
            <input
              :id="item.name"
              type="radio"
              :checked="item.checked"
              @click="() => handleRadioClick(item.value)"
              name="payment"
              :disabled="loadingInProgress"
              class="sr-only peer"
            />
            <div
              class="w-full flex gap-x-3 items-start p-4 cursor-pointer rounded-lg border bg-white shadow-sm ring-indigo-600 peer-checked:ring-2 duration-200"
            >
              <div>
                <h3 class="leading-none text-gray-800 font-medium pr-3">
                  {{ item.name }}
                </h3>
                <p class="mt-1 text-sm text-gray-600">
                  {{ item.description }}
                </p>
              </div>
            </div>
            <div
              class="absolute top-4 right-4 flex-none flex items-center justify-center w-4 h-4 rounded-full border peer-checked:bg-indigo-600 text-white peer-checked:text-white duration-200"
            >
              <svg class="w-2.5 h-2.5" viewBox="0 0 12 10">
                <polyline
                  fill="none"
                  stroke-width="2px"
                  stroke="currentColor"
                  stroke-dasharray="16px"
                  points="1.5 6 4.5 9 10.5 1"
                ></polyline>
              </svg>
            </div>
          </label>
        </li>
      </ul>
    </div>

    <div
      v-if="useOwnCredentials"
      class="w-full flex justify-center items-center"
    >
      <form
        @submit.prevent="handleFetchHighlightsClick"
        class="flex flex-col gap-y-2 w-full max-w-[600px]"
      >
        <div class="flex flex-col gap-y-1">
          <label class="text-gray-200">Email</label>
          <input
            type="email"
            required
            v-model="email"
            :disabled="loadingInProgress"
            placeholder="Enter your email"
            class="w-full px-3 py-2 text-gray-200 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg"
          />
        </div>
        <div class="flex flex-col gap-y-1">
          <label class="text-gray-200">Username</label>
          <input
            type="text"
            required
            v-model="username"
            :disabled="loadingInProgress"
            placeholder="Enter your username"
            class="w-full px-3 py-2 text-gray-200 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg"
          />
        </div>
        <div class="flex flex-col gap-y-1">
          <label class="text-gray-200">Password</label>
          <input
            type="password"
            required
            v-model="password"
            :disabled="loadingInProgress"
            placeholder="Enter your password"
            class="w-full px-3 py-2 text-gray-200 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg"
          />
        </div>
        <button
          :disabled="loadingInProgress"
          type="submit"
          class="bg-indigo-600 outline-none rounded-lg px-3 py-2 font-semibold hover:bg-indigo-700 transition-all"
        >
          {{ loadingInProgress ? "Fetching..." : "Get Highlights" }}
        </button>
      </form>
    </div>

    <div v-else class="w-full max-w-[500px]">
      <button
        @click="handleFetchHighlightsClick"
        :disabled="loadingInProgress"
        class="w-full bg-indigo-600 outline-none rounded-lg px-3 py-2 font-semibold hover:bg-indigo-700 transition-all"
      >
        {{ loadingInProgress ? "Fetching..." : "Get Highlights" }}
      </button>
    </div>

    <div v-if="error">
      <span class="text-red-600 text-[calc(16px+0.2dvw)] text-center">{{
        errorMessage
      }}</span>
    </div>

    <div v-if="highlights.length > 0" class="mt-3 flex flex-col gap-y-2">
      <div
        class="w-full max-w-[600px] rounded-lg flex flex-wrap gap-y-2 gap-x-2 items-center justify-center"
      >
        <span
          v-for="item in highlights"
          :key="item"
          class="px-3 py-2 border border-indigo-800 rounded-lg text-center hover:cursor-pointer hover:border-indigo-600 transition-all"
        >
          {{ item }}
        </span>
      </div>
      <div class="other_details metadata">
        <h3 class="font-medium">Document ID: <span class="italic font-normal">{{ newData._id }}</span></h3>
        <h3 class="font-medium">End time: <span class="italic font-normal">{{ newData.end_time }}</span></h3>
        <h3 class="font-medium">IP Address: <span class="italic font-normal">{{ newData.ip_address }}</span></h3>
      </div>
    </div>
  </body>
</template>
