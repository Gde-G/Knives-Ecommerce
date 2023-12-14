function copyToClipboard(copyId, textToCopy) {
  navigator.clipboard.writeText(textToCopy)
    .then(() => {
      let tooltip = bootstrap.Tooltip.getInstance(copyId);
      let oldTitle = tooltip._config.title 
      
      tooltip._config.title = 'Copiado!';
      tooltip.update();
      tooltip.show()

      tooltip._config.title = oldTitle;
      tooltip.update();
      
    })
    .catch(err => {
      console.error('Error al copiar: ', err);
    });
}