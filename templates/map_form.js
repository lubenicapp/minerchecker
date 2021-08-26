class Map_form
{
	static Init(){
		Map_form.onRequest = false;
		Map_form.currentTimer = {
			interval : null,
			totalTime : 0,
			i : 0
		};
	}
	/**
	 * @function Submit : Validation du formulaire
	 */

	static Submit(){
		// anti-spam
		if(Map_form.onRequest == true)
			return;
		Map_form.onRequest = true;

		clearInterval(Map_form.currentTimer.interval); // supression de l'ancien Timer si existant

		let form = Q('#form');
		let formData = new FormData(form);

		let name = formData.get('name').toLowerCase();
		let id = formData.get('id');
		let sol = formData.get('sol');

		/**@comment : animation **/

		let valider = Q('#submit');
		valider.classList.remove('on');

		let message = Q('#message p');
		message.classList.add('hide');

		let loading = Q('#loading .lds-ellipsis');
		loading.classList.add('on');

		let requete_path = SHIP_STATUS(name, id, sol);
		Requete(requete_path, null, (data)=>{
			let message = Q('#message p');
			Map.UpdatePoint(requete_path);

			setTimeout(function(){

				message.innerHTML = data;
				Map_form.StartTimer(data);
				valider.classList.add('on');
				loading.classList.remove('on');

				setTimeout(function(){
					message.classList.remove('hide');
					Map_form.onRequest = false;
				}, 200);

			}, 200);


		});
	}


	/** @functions : partie timer countdown **/

	static StartTimer(data){
		if(!/no collision/.test(data) && /collision in ([0-9]+) seconds/.test(data)){

			// initialisation
			Map_form.currentTimer.totalTime = parseInt(RegExp.$1);
			Map_form.currentTimer.i = 0;
			clearInterval(Map_form.currentTimer.interval);

			// déclenchement du timer et affichage
			Map_form.currentTimer.interval = setInterval(()=>{

				Q('#message p').innerHTML = data.replace(/collision in ([0-9]+) seconds/i, 'collision in ' + Map_form.Timer() + ' seconds');

			}, 1000);
		}
	}

	static Timer(){

		if(Map_form.currentTimer.i < Map_form.currentTimer.totalTime){
			Map_form.currentTimer.i ++;
			let diff = Map_form.currentTimer.totalTime - Map_form.currentTimer.i;
			return diff;
		}else{
			clearInterval(Map_form.currentTimer.interval);
			return 0;
		}

	}
}