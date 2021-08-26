class Map
{
	static Init(){
		Map.elmt = Q('#map');
		Map.cvs = Q('#main-canvas');
		Map.ctx = Map.cvs.getContext('2d');
		Map.InitSize();
		window.addEventListener('resize', Map.InitSize);

		// Interaction
		MapSolar.Init();
		Map.MapInteraction.Init();
		Map.cvs.addEventListener('mousedown', Map.MapInteraction.SetStartMove);
		window.addEventListener('mouseup', Map.MapInteraction.EndMove);
		Map.cvs.addEventListener('mousemove', Map.MapInteraction.GetMoveDelta);
		Map.cvs.addEventListener('wheel', Map.MapInteraction.Zoom);


		Map.bouton = {};
		Map.bouton.zoom = Q('#zoom');
		Map.bouton.recenter = Q('#recentrer');
		Map.bouton.focusShip = Q('#focus-ship');

	
		Map.bouton.recenter.addEventListener('click', ()=>{
			Map.Recentrer();
			Map.RequestDraw();
		});
		Map.bouton.focusShip.addEventListener('click', ()=>{
			Map.isFocusShip = !Map.isFocusShip;
			if(Map.isFocusShip)
				Map.bouton.focusShip.classList.add('on');
			else
				Map.bouton.focusShip.classList.remove('on');

			Map.MapInteraction.scale = 0.3;
		});

		/**@init variables**/
		Map.map_elmt = {
			red : {},
			green : {},
			blue : {}
		};
		Map.solarLimit = 60000; // rayon
		Map.isFocusShip = false;

		/** @TODO : à supprimer **/
		//Map.UpdatePoint();
	}

	static InitSize(){
		let fixedBlocSize = Q('#fixed-bloc').getBoundingClientRect();
		Map.cvs.width = fixedBlocSize.width - 50;
		Map.cvs.height = fixedBlocSize.height * 0.65;

		Map.elmt.style.width = Map.cvs.width + 'px';
		Map.elmt.style.height = Map.cvs.height*1.1 + 'px';
	}


	static Draw_Elmt(points){
		for(var nomPoint in points){
			let mapElmt = points[nomPoint];

			mapElmt.Draw({
				scale : Map.MapInteraction.scale,
				deltaMove : Map.MapInteraction.move.current
			});
		}
	}

	static Draw(){
		if(Map.isFocusShip)
			Map.FocusShip();

		Map.bouton.zoom.innerText = (Math.floor(Map.MapInteraction.scale*100*1000)/1000)/4  + '%';

		Map.ctx.clearRect(0, 0, Map.ctx.canvas.width, Map.ctx.canvas.height);

		// traçage du vaisseau vert et du soleil
		MapSolar.Draw(Map.ctx, Map.MapInteraction.move.current);

		Map.Draw_Elmt(Map.map_elmt.red);
		Map.Draw_Elmt(Map.map_elmt.blue);
		Map.Draw_Elmt({"0": Map.map_elmt.green});

	}

	static RequestDraw(){
		window.requestAnimationFrame(Map.Draw);
	}

	static Recentrer(){
		// On calcule le zoom en fonction de la taille max
		Map.MapInteraction.scale = Map.cvs.width/(Map.solarLimit*2);
		// On calcul le décalage pour centrer le système solaire
		Map.MapInteraction.move.current = {
			x : Map.cvs.width / 2 ,
			y : Map.cvs.height / 2
		}
	}

	static FocusShip(){
		Map.MapInteraction.move.current = {
			x : -Map.map_elmt.green.km.x * Map.MapInteraction.scale + Map.cvs.width / 2,
			y : -Map.map_elmt.green.km.y * Map.MapInteraction.scale + Map.cvs.height / 2
		};
	}

	static UpdatePoint_AddData(type, color, nomPoint, json){
		let data = json[nomPoint];
		Map.map_elmt[type][nomPoint] = new Map_Square(data, color, Map.ctx);
	}

	static UpdatePoint(prefix_path){
		Requete(prefix_path+MAP_COORD.red, null, (jsonRed)=>{
		Requete(prefix_path+MAP_COORD.green, null, (jsonGreen)=>{
		Requete(prefix_path+MAP_COORD.blue, null, (jsonBlue)=>{
			let json = {
				red : jsonRed,
				ship : jsonGreen,
				blue : jsonBlue
			};

			Map.map_elmt = {
				red : {},
				green : {},
				blue : {}
			};

			for(var nomPoint in json.red){
				Map.UpdatePoint_AddData('red', '#ff0000', nomPoint, json.red);
			}

			for(var nomPoint in json.blue){
				Map.UpdatePoint_AddData('blue', '#62c2fe', nomPoint, json.blue);
			}

			Map.map_elmt.green = new Map_Ship(jsonGreen, Map.ctx);
			Map.Recentrer();

			Map.MapCalcul.Init();
			Map.RequestDraw();
			
		});
		});
		});
	}

	static MapCalcul = class MapCalcul
	{	

		static Init(){
			MapCalcul.tempsEcoule = new Date().getTime()/1000; // temps en secondes écoulé depuis la dernière sauvegarde
			setTimeout(MapCalcul.Update, 1000);
		}

		static Update_Loop(points){
			for(var nomPoint in points){
				let mapElmt = points[nomPoint];
				let newPosition = MapCalcul.ComputePositionAt(mapElmt, new Date().getTime()/1000);
				
				//mapElmt.timestamp = newPosition.ts; // udpate du ts car on udpate le x et y de mapElmt
				mapElmt.SetPosition(newPosition);
			}
		}

		static Update(){

			let delta = Math.floor(new Date().getTime()/1000 - MapCalcul.tempsEcoule);
			if(Map.map_elmt.red[delta])
				delete Map.map_elmt.red[delta];

			MapCalcul.Update_Loop({"0": Map.map_elmt.green});
			MapCalcul.Update_Loop(Map.map_elmt.blue);
			MapCalcul.Update_Loop(Map.map_elmt.red);
			Map.RequestDraw();
			setTimeout(MapCalcul.Update, 1000);
			//window.requestAnimationFrame(MapCalcul.Update);
		}

		/**
		 * @function ComputePositionAt
		 * @param {string} type : red, green, blue
		 * @param {string} nomPoint : nom/numéro du point
		 * @param {int} ts : timestamp actuel demandé en seconde
		 */
		static ComputePositionAt(mapElmt, ts){
			let position = mapElmt.startKm;
			let t = mapElmt.timestamp;
			let angle = 0;
			let angle_2 = 0;

			let distance = Math.sqrt(Math.pow(position.x, 2) + Math.pow(position.y, 2));
			if(distance != 0){
				angle = Math.atan2(position.y, position.x);
				angle_2 = angle + (ts - t) * 3 / distance;
			}

			let position2 = {
				x : parseInt(distance * Math.cos(angle_2)),
				y : parseInt(distance * Math.sin(angle_2))
			};

			return {...position2, ts};
		}
	}

	/** Map intéraction fonctionnalité **/
	static MapInteraction = class MapInteraction
	{
		static Init(){
			
			MapInteraction.move = {
				isMoving : false,
				current : { x:0, y:0 }, // le décalage actuel de la map
				start : { x:0, y:0 },
				global : { x:0, y:0 } // pour changer l'origine du repère (un zoom non centré sur le soleil)
			};
			MapInteraction.scale = 1;

		}

		static SetStartMove(e){
			MapInteraction.move.start.x = e.clientX;
			MapInteraction.move.start.y = e.clientY;
			MapInteraction.move.isMoving = true;
		}
		static EndMove(){
			MapInteraction.move.isMoving = false;
		}

		static GetMoveDelta(e){
			let move = MapInteraction.move;
			if(!move.isMoving)return;

			let delta = {
				x : e.clientX - move.start.x,
				y : e.clientY - move.start.y
			};

			move.start.x = e.clientX;
			move.start.y = e.clientY;

			MapInteraction.ApplyMove(delta);
		}

		static ApplyMove(delta){
			MapInteraction.move.current.x += delta.x;
			MapInteraction.move.current.y += delta.y;
			Map.RequestDraw();
		}

		static Zoom(e){
			e.preventDefault();
			
			// 1/ calcule du zoom/scale
			let deltaVal = 0;
			// A partir de 0.3%, on dé
			if(MapInteraction.scale <= 0.3 / 100)
				deltaVal = e.deltaY * -0.000001;
			else if(MapInteraction.scale <= 7 / 100)
				deltaVal = e.deltaY * -0.00001;
			else if(MapInteraction.scale <= 50 / 100)
				deltaVal = e.deltaY * -0.0001;
			else
				deltaVal = e.deltaY * -0.001;

			MapInteraction.scale += deltaVal;
			MapInteraction.scale = Math.min(Math.max(.000001, MapInteraction.scale), 4);
			MapInteraction.ApplyMove({ x:0, y:0 });
		}

	}

}

class MapSolar
{
	static Init(){
		MapSolar.move = { x:0, y:0 };
	}
	static Draw(ctx, deltaMove){
		MapSolar.move.x = deltaMove.x;
		MapSolar.move.y = deltaMove.y;

		ctx.save();
		ctx.beginPath();

		ctx.shadowColor = 'yellow';
		ctx.shadowBlur = 20;

		ctx.fillStyle = 'yellow';
		ctx.arc(MapSolar.move.x, MapSolar.move.y, 25, 0, 2*Math.PI);
		ctx.fill();

		// limite système solaire
		// ctx.shadowBlur = 5;
		// ctx.shadowColor = '#781294';
		// ctx.strokeStyle = '#781294';
		// ctx.beginPath();
		// ctx.arc(MapSolar.move.x, MapSolar.move.y, Map.solarLimit*Map.MapInteraction.scale, 0, 2*Math.PI);
		// ctx.stroke();
		//
		// ctx.beginPath();
		// ctx.arc(MapSolar.move.x, MapSolar.move.y, (Map.solarLimit-10000)*Map.MapInteraction.scale, 0, 2*Math.PI);
		// ctx.stroke();
		//
		ctx.restore();
	}
}

class MapElmt
{
	constructor(data, ctx){
		this.ctx = ctx;
		this.startKm = { x : data[0], y : data[1] };
		this.km = { x : 0, y : 0 };
		this.size = { x : 10, y : 10 };
		this.SetPosition(this.startKm);
		this.timestamp = data[2];
		this.bgColor = '#fff';
	}

	SetPosition(val){
		this.km = {
			x : val.x,
			y : val.y
		};
	}

	GetPosition(scale){
		return {
			x : this.km.x * scale,
			y : this.km.y * scale
		};
	}

	Draw(obj){
		let position = this.GetPosition(obj.scale);
		position.x += Map.MapInteraction.move.global.x;
		position.y += Map.MapInteraction.move.global.y

		return position;
	}

}

class Map_Square extends MapElmt
{
	constructor(data, color, ctx){
		super(data, ctx);
		this.bgColor = color;
	}

	Draw(obj){
		let position = super.Draw(obj);
			
		position.x += obj.deltaMove.x;
		position.y += obj.deltaMove.y;

		this.ctx.save();
		this.ctx.shadowColor = 'rgba(0,0,0,0.4)';
		this.ctx.shadowBlur = 5;
		this.ctx.fillStyle = this.bgColor;
		this.ctx.fillRect(position.x, position.y, this.size.x, this.size.y);

		/*this.ctx.strokeStyle = '#000';
		this.ctx.strokeRect(position.x, position.y, size.x, size.y);*/
		this.ctx.restore();
		this.ctx.fillStyle = 'red';

		return position;
	}
}

class Map_Ship extends Map_Square
{
	constructor(data, ctx, radius){
		super(data.ship, '#68d807', ctx);
		this.radius = data.radius;
	}
	Draw(obj){
		let position = super.Draw(obj);
		let scale = Map.MapInteraction.scale;

		// pour avoir comme centre le pixel vaisseau
		position.x += this.size.x/2;
		position.y += this.size.y/2;

		this.ctx.save();

		this.ctx.strokeStyle = 'rgb(97, 192, 254)';
		this.ctx.fillStyle = 'rgba(97, 192, 254, 0.4)';
		this.ctx.beginPath();
		this.ctx.arc(position.x, position.y, this.radius * scale, 0, 2 * Math.PI);
		this.ctx.stroke();
		this.ctx.fill();

		this.ctx.restore();
	}
}