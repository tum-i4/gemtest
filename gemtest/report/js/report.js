window.metamorphic = {
    toggleFullError(errorId) {
        const normalError = document.getElementById(errorId);
        const fullError = document.getElementById(`${errorId}_full`);
        normalError.classList.toggle('metamorphic__hidden');
        fullError.classList.toggle('metamorphic__hidden');
    }
};