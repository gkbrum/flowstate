from pydantic import BaseModel, ConfigDict, Field, model_validator

class PlaylistDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    
    playlist_id: str = Field(alias="id")
    name: str
    cover_url: str
    public: bool
    tracks_url: str
    total_tracks: int
    
    @model_validator(mode="before")
    @classmethod
    def flatten_dict(cls, data):
        
        if(isinstance(data,dict)):  #verificação caso o pydantic tenha injetado algum outro objeto
            
            #atribui os valores que a api retorna para chaves que o pydantic pode achar e injetar na classe
            data["tracks_url"] = data["items"]["href"]
            data["total_tracks"] = data["items"]["total"]
            
            if data.get("images") and len(data["images"]) > 0:  #verifica se o array de imagens esta vazio e se a chave nao é nula
                data["cover_url"] = data["images"][0]["url"]
        
        return data
    
             
            