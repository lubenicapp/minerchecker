/**
 * @comment : les constantes de requêtes (url) à modifier si besoin
 */




const SHIP_LIST = '/ships';
const SHIP_STATUS = function(name, id, sol){
	return '/'+name+'/'+id+'/'+sol;
};
const SHIP_CARAC = '/carac';


/**
 * @function RequeteJSON : pour récupérer des données JSON sur le serveur
 * @param {string} url : cible
 * @param {function} callback : fonction de retour une fois requete fini
 */

function Requete(url, params, callback){
	fetch(url, params)
		.then(rep=>{
			if(rep.ok){
				rep.text().then(text=>{
					try{
						let json = JSON.parse(text);
						callback(json);
					}catch(err){
						callback(text);
					}
				});
			}else{
				throw new Error();
			}
		});

}


/**
 * @function Elmt : permet de créer un élément HTML avec des attributs
 * @param {string} type : nom de la balise HTML
 * @param {Object} o : objet contenant tous les attributs à assigner à l'élément crée
 */

function Elmt(type, o){
	var elmt = document.createElement(type);

	if(o.class){
		o.class.forEach(nameClass=>{
			elmt.classList.add(nameClass);
		});
		delete o.class;
	}

	for(var key in o){
		elmt[key] = o[key];
	}

	o.parent.appendChild(elmt);

	return elmt;
}

/**
 * @function Q : raccourci de querySelector
 */

const Q = elmt=>document.querySelector(elmt);




/**
 * ##############################
 * @comment : fin de la partie des fonctions "globaux"
 * ##############################
 */


/**
 * @function Ships : créer les petites cartes cliquables pour remplir le champ
 */

function Ships(ships, parent){

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
var collections = null;
var carac = {};
function Collections(json){
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

		Ships(collection.ships, ctn);
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


/**
 * @function Submit : Validation du formulaire
 */
var onRequest = false;
function Submit(){

	// anti-spam
	if(onRequest == true)
		return;
	onRequest = true;

	clearInterval(currentTimer.interval); // supression de l'ancien Timer si existant

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


	Requete(SHIP_STATUS(name, id, sol), null, (data)=>{
		let message = Q('#message p');

		setTimeout(function(){

			message.innerHTML = data;
			StartTimer(data);
			valider.classList.add('on');
			loading.classList.remove('on');

			setTimeout(function(){
				message.classList.remove('hide');
				onRequest = false;
			}, 200);

		}, 200);

	});
}


var currentTimer = {
	interval : null,
	totalTime : 0,
	i : 0
};
function StartTimer(data){
	if(!/no collision/.test(data) && /collision in ([0-9]+) seconds/.test(data)){

		// initialisation
		currentTimer.totalTime = parseInt(RegExp.$1);
		currentTimer.i = 0;
		clearInterval(currentTimer.interval);

		// déclenchement du timer et affichage
		currentTimer.interval = setInterval(()=>{

			Q('#message p').innerHTML = data.replace(/collision in ([0-9]+) seconds/i, 'collision in ' + Timer() + ' seconds');

		}, 1000);
	}
}

function Timer(){

	if(currentTimer.i < currentTimer.totalTime){
		currentTimer.i ++;
		let diff = currentTimer.totalTime - currentTimer.i;
		return diff;
	}else{
		clearInterval(currentTimer.interval);
		return 0;
	}

}


/**
 * @event : Quand la page est prête, nous récupérons sur le serveur la liste des vaisseaux
 */
document.addEventListener('DOMContentLoaded', ()=>{

	Requete(SHIP_CARAC, null, (json)=>{
		carac = json;
		Requete(SHIP_LIST, null, Collections);
	});

	Q('#form').addEventListener('submit', (e)=>{
		e.preventDefault();
		Submit();
	})


});

