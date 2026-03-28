<template>
    <div class="pa-md-4 pa-2">
        <h1 class="mb-2 text-center text-h4 text-md-h3 font-weight-bold">Leitura do Alcorão</h1>
        <p class="text-center text-subtitle2 text-md-subtitle1 mb-8 text-grey-darken-1">Explore os versículos sagrados
        </p>

        <div v-if="ayats.length" class="mt-8">
            <v-card v-for="ayat in ayats" :key="ayat.id" class="mb-4" elevation="2" hover>
                <v-card-text class="py-6 px-4 px-md-6">
                    <div class="d-flex flex-column flex-md-row gap-4 align-md-center">
                        <v-row>
                            <v-col>
                                <div class="flex-grow-1 min-w-0">
                                    <div class="d-flex align-start gap-3 mb-2">
                                        <v-chip color="success" text-color="white" size="small"
                                            class="font-weight-bold flex-shrink-0 text-center align-center justify-center">
                                            {{ ayat.number }}
                                        </v-chip>
                                    </div>
                                    <p class="text-body1 text-md-h6 mb-0 text-justify text-white"
                                        style="line-height: 1.8; letter-spacing: 0.3px;">
                                        {{ ayat.text }}
                                    </p>
                                </div>

                                <v-divider class="ma-4" />

                                <!-- Botões de Ação -->
                                <div class="d-flex justify-center gap-3">
                                    <v-btn icon="mdi-content-copy" size="large" variant="text" color="success"
                                        @click="copyToClipboard(ayat.text, ayat)" title="Copiar versículo">
                                    </v-btn>

                                    <v-btn icon="mdi-volume-high" size="large" variant="text" color="success"
                                        @click="speakAyat(ayat.text)" :disabled="isSpeaking" title="Ler em voz alta">
                                    </v-btn>
                                </div>
                            </v-col>
                        </v-row>
                    </div>
                </v-card-text>
            </v-card>
        </div>

        <v-empty-state v-else icon="mdi-book-open-page-variant" headline="Nenhum versículo carregado"
            text="Os versículos aparecerão aqui" />
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import localforage from 'localforage';

interface Ayat {
    id: number;
    number: number;
    text: string;
}

const ayats = ref<Ayat[]>([]);
const isSpeaking = ref(false);

const speakAyat = (text: string) => {
    if (!('speechSynthesis' in window)) {
        alert('Seu navegador não suporta leitura em voz alta.');
        return;
    }

    // Cancela tudo antes
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    // Configurações mínimas e mais estáveis
    utterance.lang = 'pt-BR';
    utterance.rate = 0.9;      // mais lento ajuda
    utterance.pitch = 1.0;
    utterance.volume = 0.9;    // volume ligeiramente baixo às vezes ajuda

    // Removemos completamente a seleção de voz (causa comum do erro)

    utterance.onend = () => isSpeaking.value = false;

    utterance.onerror = (event) => {
        isSpeaking.value = false;
        console.error('SpeechSynthesis Error:', event.error);

        if (event.error === 'synthesis-failed') {
            alert('Falha ao iniciar a voz.\n\nDicas:\n• Tente usar o Chrome ou Edge\n• Recarregue a página\n• Teste em outro computador');
        } else {
            alert('Não foi possível reproduzir o áudio.');
        }
    };

    isSpeaking.value = true;

    // Delay pequeno + retry simples
    setTimeout(() => {
        try {
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            isSpeaking.value = false;
            alert('Erro ao tentar falar. Recarregue a página.');
        }
    }, 100);
};

const copyToClipboard = async (text: string, ayat: Ayat) => {
    const selectedChapter = Number((await localforage.getItem('selectedChapter')) || 1);
    const formattedText = `"${text}"\n\n(Alcorão, Capítulo ${selectedChapter}, Versículo ${ayat.number})`;

    navigator.clipboard.writeText(formattedText).then(() => {
        alert('Versículo copiado!');
    });
};

onMounted(() => {
    ayats.value = [
        { id: 1, number: 1, text: "Alif, Lam, Mim." },
        { id: 2, number: 2, text: "Esse é o Livro, sem dúvida, é uma direção para os que temem a Allah." },
        { id: 3, number: 3, text: "Os que creem no invisível, estabelecem a oração e gastam em beneficência, do que lhes providenciamos." }
    ];

    // Tenta carregar vozes
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
        setTimeout(() => window.speechSynthesis.getVoices(), 800);
    }
});
</script>