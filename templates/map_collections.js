class Map_collections
{
	static Init(){
		Map_collections.collections = null;
		Map_collections.carac = {};
	}

	/**
	 * @function Ships : créer les petites cartes cliquables pour remplir le champ
	 */

	static _Ships(ships, parent){

		ships.forEach(ship=>{

			let bloc = Elmt('div', {
				class : ['ship'],
				parent : parent
			});

			bloc.addEventListener('click', ()=>{
				Q('#ship_name').value = ship;
				/** @comment : Système d'ajout par click des caractérisques **/
				/*let val = prompt("Shipname : " + ship + " | Taper : mRange mPower cooldown (sans unité, et 1 espace pour séparé les valeurs, les modfis s'afficheront dans la console Javascript du navigateur");
				let vals = val.split(' ');

				carac[ship].MINING_RANGE = parseFloat(vals[0]);
				carac[ship].MINING_POWER = parseFloat(vals[1]);
				carac[ship].COOLDOWN = parseFloat(vals[2]);
				console.log(ship, carac[ship]);*/
			});

			let ctn = Elmt('div', {
				class : ['ctn-img'],
				parent : bloc
			});

			let img = Elmt('img', {
				src : 'ships_img/' + ship.replace(/ /i, '_') + '.png',
				parent : ctn
			});

			let texte = Elmt('p', {
				innerText : ship,
				parent : bloc,
				class : ['ship-name']
			});

			/** @comment : rajout des caractéristiques **/
			let currentCarac = carac[ship];
			let table = Elmt('table', {
				parent : bloc,
				class : ['carac']
			});

			function LigneTableau(table, caracNom, valeur){
				let tr = Elmt('tr', {
					parent : table
				});
				Elmt('td', {
					parent : tr,
					innerHTML : caracNom.replace(/_/, ' ')
				});
				Elmt('td', {
					parent : tr,
					innerHTML : valeur
				});
			}



			LigneTableau(table, 'mining range', currentCarac.MINING_RANGE+' km');
			LigneTableau(table, 'mining power', currentCarac.MINING_POWER+' %');
			LigneTableau(table, 'cooldown', currentCarac.COOLDOWN+' s');
		});

	}


	/**
	 * @function Collection : établie la liste des vaisseaux par collection
	 */

	static _Collections(json){
		json.collections.forEach(collection=>{
			let ctn = Elmt('div', {
				class : ['collection'],
				parent : Q('#list-container'),

			});

			let titre = Elmt('h1', {
				class : ['titre'],
				parent : ctn,
				innerText : collection.name
			});

			Map_collections._Ships(collection.ships, ctn);
		});

		setTimeout(function(){
			let ctnImg = Array.from(document.querySelectorAll('.ctn-img img'));
			let casParticulier = ctnImg.slice(ctnImg.length-8, ctnImg.length);

			casParticulier.forEach(cas=>{
				cas.classList.add('cas-particulier');
			});
		}, 1000);

		/** @comment : Pour le Système d'ajout par click des caractérisques **/
		/*collections = json.collections.slice();
		collections.forEach(col=>{
			col.ships.forEach(shipName=>{
				carac[shipName] = {
					MINING_RANGE : 0,
					MINING_POWER : 0,
					COOLDOWN : 0
				}
			});
		});*/

	}
}

