<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>

    <BottomNavigation />
  </v-app>
</template>

<script setup>
import BottomNavigation from '@/components/BottomNavigation.vue'
</script>
