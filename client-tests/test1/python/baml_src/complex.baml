function ClassifyTool {
  input (query: string, context: string)
  output ClassifyResponse
}
 
class ClassifyResponse { 
  tool Tool[] @description(#"
    Any number of tools the user may want to use
  "#)
  assistant_response string 
  
  pretty_message string @get(
    python#"
      import json
      from xyz import xyz

      thingy = []
      # iterate over stuff
      json.loads()
      return f'You can use the following tools: {self.tool}'
    "#
  )

    
  pretty_message2 string @get(
    python#"
      import json
      from xyz import xyz

      thingy = []
      # iterate over stuff
      json.loads()
      return f'You can use the following tools: {self.tool}'
    "#
  )
}

enum Tool {
  @@alias(tools)
  
  CodeInterpreter
  @alias(k1) 
  @description(Use this tool if the user is asking to compute something)

  DrawImage
  @alias(k2) 
  @description(Use this tool if the user is asking to draw something)

  GenerateText 
  @alias(k3)
  @description(Use this tool if the user is asking to generate text)
}

 
 
impl<llm, ClassifyTool> v1 {
    client AZURE_GPT4

    override Tool {
      @@alias(tool)
    }

    override ClassifyResponse {
      assistant_response @alias(foo)
      @description(#"
        This is the assistance reponse
      "#)
    }

    prompt #"
        
        {#input.query}
 
        UserContext:
        {#input.context}
  
        {#print_enum(Tool)} 

        Use this output format:
        {#print_type(output)}

        JSON:
    "#

}