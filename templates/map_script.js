/**
 * @comment : les constantes de requêtes (url) à modifier si besoin
 */


const SHIP_LIST = '/ships';
const SHIP_STATUS = function(name, id, sol){
    return '/'+name+'/'+id+'/'+sol;
};
const SHIP_CARAC = '/carac';
const MAP_COORD = {
    red : '/red',
    green : '/green',
    blue : '/blue'
};

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
                        console.error(err, text)
                        callback(text);
                    }
                });
            }else{
                throw new Error();
            }
        })
        .catch(err=>{
            console.error(err)
        })
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

/** @function Q : raccourci de querySelector **/
const Q = elmt=>document.querySelector(elmt);


/**
 * ##############################
 * @comment : fin de la partie des fonctions "globaux"
 * ##############################
 */





/**
 * @event : Quand la page est prête, nous récupérons sur le serveur la liste des vaisseaux
 */
document.addEventListener('DOMContentLoaded', ()=>{

    Map_collections.Init();
    Map.Init();
    Map_form.Init();

    Requete(SHIP_CARAC, null, (json)=>{
        carac = json;
        Requete(SHIP_LIST, null, Map_collections._Collections);
    });

    Q('#form').addEventListener('submit', (e)=>{
        e.preventDefault();
        Map_form.Submit();
    })


});