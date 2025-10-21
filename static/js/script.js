document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById('startBtn');
    const fotoBtn = document.getElementById('fotoBtn');
    const videoCamara = document.getElementById('videoCamara');
    const estadoCamara = document.querySelector('.estado');
    const fotoCapturada = document.getElementById('fotoCapturada');
    const emocionEnCamara = document.getElementById('emocionEnCamara');

    const felizEl = document.getElementById('feliz');
    const tristeEl = document.getElementById('triste');
    const neutralEl = document.getElementById('neutral');
    const enojadoEl = document.getElementById('enojado');
    const sorprendidoEl = document.getElementById('sorprendido');
    const sinreconocerEl = document.getElementById('sinreconocer');

    const estadoEl = document.getElementById('estado');
    const porcentajeEl = document.getElementById('porcentaje');
    const rostroEl = document.getElementById('rostro');
    const sujetoEl = document.getElementById('sujeto');

    let stream = null;
    let camaraEncendida = false;
    let segundos = { Feliz:0, Triste:0, Neutral:0, Enojado:0, Sorprendido:0, SinReconocer:0 };
    let intervalo = null;

    startBtn.addEventListener('click', async () => {
        if (!camaraEncendida) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                videoCamara.srcObject = stream;
                estadoCamara.textContent = 'Cámara activa';
                camaraEncendida = true;
                startBtn.textContent = 'Apagar Cámara';
                fotoBtn.disabled = false;

                // Inicia predicción cada 1 segundo
                intervalo = setInterval(capturarYPredecir, 1000);

            } catch (err) {
                console.error("Error al iniciar cámara:", err);
                estadoCamara.textContent = 'Error al iniciar cámara';
            }
        } else {
            // Apagar cámara
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            videoCamara.srcObject = null;
            estadoCamara.textContent = 'Apagado';
            camaraEncendida = false;
            startBtn.textContent = 'Iniciar Cámara';
            fotoBtn.disabled = true;

            if (intervalo) clearInterval(intervalo);
        }
    });

    function capturarYPredecir() {
        const canvas = document.createElement('canvas');
        const size = 220;
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');
        const vw = videoCamara.videoWidth;
        const vh = videoCamara.videoHeight;
        const sx = (vw - size) / 2;
        const sy = (vh - size) / 2;
        ctx.drawImage(videoCamara, sx, sy, size, size, 0, 0, size, size);

        const fotoBase64 = canvas.toDataURL('image/png');
        fotoCapturada.src = fotoBase64;

        fetch("/predict_emotion", {  // Aquí apunta al backend Flask o Django
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: fotoBase64 })
        })
        .then(res => res.json())
        .then(data => {
            let emocion = data.label || "SinReconocer";
            const confianza = data.confidence || 0;

            if (!["Feliz","Triste","Neutral","Enojado","Sorprendido"].includes(emocion)) {
                emocion = "SinReconocer";
            }

            // Mostrar emoción en la cámara
            emocionEnCamara.textContent = `${emocion} — ${confianza.toFixed(1)}%`;

            // Actualizar informe
            estadoEl.textContent = `Estado: ${emocion}`;
            porcentajeEl.textContent = `Porcentaje: ${confianza.toFixed(1)}%`;
            rostroEl.textContent = `Estado del rostro: Detectado`;
            sujetoEl.textContent = `Id: 001`;

            // Sumar segundos
            if (emocion in segundos) segundos[emocion] += 1;

            felizEl.textContent = `Feliz: ${segundos.Feliz} seg`;
            tristeEl.textContent = `Triste: ${segundos.Triste} seg`;
            neutralEl.textContent = `Neutral: ${segundos.Neutral} seg`;
            enojadoEl.textContent = `Enojado: ${segundos.Enojado} seg`;
            sorprendidoEl.textContent = `Sorprendido: ${segundos.Sorprendido} seg`;
            sinreconocerEl.textContent = `Sin reconocer: ${segundos.SinReconocer} seg`;
        })
        .catch(err => console.error("Error predicción:", err));
    }
});
