<template>
  <div class="pa-4">
    <h1 class="mb-6 text-center">Capítulos do Alcorão ☪️</h1>
    <v-row>
      <v-col v-for="chapter in chapters" :key="chapter.id" cols="6" sm="6" md="4" lg="3">
        <v-btn class="h-100 w-100 pa-4" :variant="selectedChapter === chapter.id ? 'elevated' : 'flat'"
          :color="selectedChapter === chapter.id ? 'success' : 'default'" size="x-large"
          @click="selectChapter(chapter.id)">
          <div class="text-center">
            <div class="text-h5 font-weight-bold">{{ chapter.id }}</div>
            <div class="text-subtitle2">{{ chapter.name }}</div>
          </div>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import localforage from 'localforage'
import router from '@/router'

interface Chapter {
  id: number
  name: string
}

const chapters = ref<Chapter[]>([
  { id: 1, name: 'A Abertura' },
  { id: 2, name: 'A Vaca' },
  { id: 3, name: 'A Família de Imrã' },
  { id: 4, name: 'As Mulheres' },
  { id: 5, name: 'A Mesa' },
  { id: 6, name: 'Os Rebanhos' },
  { id: 7, name: 'As Alturas' },
  { id: 8, name: 'O Saque' },
  { id: 9, name: 'O Arrependimento' },
  { id: 10, name: 'Jonas' },
  { id: 11, name: 'Hud' },
  { id: 12, name: 'José' },
  { id: 13, name: 'O Trovão' },
  { id: 14, name: 'Abraão' },
  { id: 15, name: 'A Pedra Preciosa' },
  { id: 16, name: 'As Abelhas' },
  { id: 17, name: 'A Jornada Noturna' },
  { id: 18, name: 'A Caverna' },
  { id: 19, name: 'Maria' },
  { id: 20, name: 'Tá Há' },
  { id: 21, name: 'Os Profetas' },
  { id: 22, name: 'A Peregrinação' },
  { id: 23, name: 'Os Crentes' },
  { id: 24, name: 'A Luz' },
  { id: 25, name: 'O Critério' },
  { id: 26, name: 'Os Poetas' },
  { id: 27, name: 'As Formigas' },
  { id: 28, name: 'A História' },
  { id: 29, name: 'A Aranha' },
  { id: 30, name: 'Os Romanos' },
  { id: 31, name: 'Luqmã' },
  { id: 32, name: 'A Prostração' },
  { id: 33, name: 'Os Coligados' },
  { id: 34, name: 'Sabá' },
  { id: 35, name: 'O Criador' },
  { id: 36, name: 'Yá Sín' },
  { id: 37, name: 'Os Que Se Alinham' },
  { id: 38, name: 'Sá' },
  { id: 39, name: 'Os Grupos' },
  { id: 40, name: 'O Perdoador' },
  { id: 41, name: 'Os Versículos Explicados' },
  { id: 42, name: 'A Consulta' },
  { id: 43, name: 'O Ornamento' },
  { id: 44, name: 'A Fumaça' },
  { id: 45, name: 'O Ajoelhamento' },
  { id: 46, name: 'As Dunas' },
  { id: 47, name: 'Muhammad' },
  { id: 48, name: 'A Vitória Aberta' },
  { id: 49, name: 'Os Aposentos' },
  { id: 50, name: 'Qá' },
  { id: 51, name: 'Os Que Disseminam' },
  { id: 52, name: 'O Monte' },
  { id: 53, name: 'A Estrela' },
  { id: 54, name: 'A Lua' },
  { id: 55, name: 'O Misericordioso' },
  { id: 56, name: 'O Evento Inevitável' },
  { id: 57, name: 'O Ferro' },
  { id: 58, name: 'A Discussão' },
  { id: 59, name: 'O Banimento' },
  { id: 60, name: 'A Mulher Posta à Prova' },
  { id: 61, name: 'A Fileira' },
  { id: 62, name: 'A Congregação' },
  { id: 63, name: 'Os Hipócritas' },
  { id: 64, name: 'O Engano Mútuo' },
  { id: 65, name: 'O Divórcio' },
  { id: 66, name: 'A Proibição' },
  { id: 67, name: 'A Realeza' },
  { id: 68, name: 'A Pena' },
  { id: 69, name: 'A Hora Inevitável' },
  { id: 70, name: 'Os Degraus' },
  { id: 71, name: 'Noé' },
  { id: 72, name: 'Os Gênios' },
  { id: 73, name: 'O Envolto em Manto' },
  { id: 74, name: 'O Coberto de Roupa' },
  { id: 75, name: 'A Ressurreição' },
  { id: 76, name: 'O Ser Humano' },
  { id: 77, name: 'Os Enfiados' },
  { id: 78, name: 'A Notícia' },
  { id: 79, name: 'Os Que Arrancam' },
  { id: 80, name: 'Ele Franziu a Testa' },
  { id: 81, name: 'O Enrolamento' },
  { id: 82, name: 'Os Que Clivam' },
  { id: 83, name: 'Os Defraudadores' },
  { id: 84, name: 'O Rasgamento' },
  { id: 85, name: 'As Constelações' },
  { id: 86, name: 'A Estrela Noturna' },
  { id: 87, name: 'O Altíssimo' },
  { id: 88, name: 'O Coberto de Obscuridade' },
  { id: 89, name: 'A Aurora' },
  { id: 90, name: 'A Cidade' },
  { id: 91, name: 'O Sol' },
  { id: 92, name: 'A Noite' },
  { id: 93, name: 'A Claridade Matinal' },
  { id: 94, name: 'A Abertura do Peito' },
  { id: 95, name: 'A Figueira' },
  { id: 96, name: 'O Coágulo' },
  { id: 97, name: 'O Poder' },
  { id: 98, name: 'A Prova Clara' },
  { id: 99, name: 'O Terremoto' },
  { id: 100, name: 'Os Cavalos Galopantes' },
  { id: 101, name: 'O Estrondo' },
  { id: 102, name: 'A Distração no Acúmulo de Bens' },
  { id: 103, name: 'A Tarde' },
  { id: 104, name: 'O Difamador' },
  { id: 105, name: 'O Elefante' },
  { id: 106, name: 'Os Coraixitas' },
  { id: 107, name: 'As Coisas Pequenas' },
  { id: 108, name: 'A Abundância' },
  { id: 109, name: 'Os Descrentes' },
  { id: 110, name: 'O Auxílio' },
  { id: 111, name: 'As Fibras' },
  { id: 112, name: 'A Sinceridade da Fé' },
  { id: 113, name: 'O Amanhecer' },
  { id: 114, name: 'Os Homens' },
])

const selectedChapter = ref<number>(1)

onMounted(async () => {
  const saved = await localforage.getItem<number>('selectedChapter')
  if (saved) {
    selectedChapter.value = saved
  }
})

const selectChapter = async (chapterId: number) => {
  selectedChapter.value = chapterId
  await localforage.setItem('selectedChapter', chapterId)

  router.push('/reading');
}
</script>
